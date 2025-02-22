import logging
import json

from collections import defaultdict

from squad.core.models import SuiteMetadata, Test, KnownIssue, Status, TestRun, PluginScratch
from squad.celery import app as celery
from squad.core.utils import join_name, split_dict
from squad.core.tasks import RecordTestRunStatus
from squad.ci.tasks import update_testjob_status


logger = logging.getLogger()


@celery.task(queue='ci_fetch')
def update_build_status(results_list, testrun_id, job_id, job_status):

    """
        There could be a scenario where the test job, and its test run as consequence, gets deleted
        by the user. Since this function is invoked upon task from the queue, by the time it actually
        gets invoked, the test run might not exist anymore.
    """
    try:
        testrun = TestRun.objects.get(pk=testrun_id)
    except TestRun.DoesNotExist:
        return

    # Compute stats all at once
    Status.objects.filter(test_run=testrun).all().delete()
    testrun.status_recorded = False
    RecordTestRunStatus()(testrun)

    update_testjob_status.delay(job_id, job_status)


@celery.task(queue='ci_fetch')
def create_testcase_tests(pluginscratch_id, suite_slug, testrun_id):
    try:
        scratch = PluginScratch.objects.get(pk=pluginscratch_id)
        test_cases = json.loads(scratch.storage)
    except PluginScratch.DoesNotExist:
        logger.error(f"PluginScratch with ID: {pluginscratch_id} doesn't exist")
        return
    except ValueError as e:
        logger.error(f"Failed to load json for PluginScratch ({pluginscratch_id}): {e}")

    testrun = TestRun.objects.get(pk=testrun_id)
    issues = defaultdict(list)
    for issue in KnownIssue.active_by_environment(testrun.environment):
        issues[issue.test_name].append(issue)

    suite = testrun.build.project.suites.get(slug=suite_slug)

    try:
        test_names = {}
        for test_case in test_cases:
            test_case_name = test_case.get("name")

            tests = test_case['tests']
            logger.debug(f"Extracting TestCase: {test_case_name} - {len(tests)} testcases")
            for test in tests:

                test_result = None
                if test.get("result") == "pass":
                    test_result = True
                elif test.get("result") in ["fail", "ASSUMPTION_FAILURE"]:
                    test_result = False

                test_name = f"{test_case_name}.{test.get('name')}"

                # TODO: increase SQUAD's max length for test name
                #       currently it's at 256 characters
                test_name = test_name[:256]

                full_name = join_name(suite_slug, test_name)
                test_issues = issues.get(full_name, [])

                # Collect test details to add in bulk to the database
                test_names[test_name] = {
                    "result": test_result,
                    "log": test.get('log', ''),
                    "has_known_issues": bool(test_issues),
                }

        batch_size = 1000
        for batch in split_dict(test_names, batch_size):
            # Create SuiteMetadata in bulk
            SuiteMetadata.objects.bulk_create([
                SuiteMetadata(
                    suite=suite_slug,
                    name=test_name,
                    kind='test',
                ) for test_name in batch
            ], ignore_conflicts=True)

            # We need the extra SELECT due to `ignore_conflicts=True` above
            metadata_ids = {}
            metadata_names = {}
            for metadata in SuiteMetadata.objects.filter(suite=suite_slug, name__in=list(batch)).all():
                if metadata.kind != 'test':
                    continue

                metadata_ids[metadata.name] = metadata.id
                metadata_names[metadata.id] = metadata

            # Create tests in batch
            created_tests = Test.objects.bulk_create([
                Test(
                    test_run=testrun,
                    suite=suite,
                    metadata_id=metadata_ids[test_name],
                    result=test_values["result"],
                    log=test_values["log"],
                    has_known_issues=test_values["has_known_issues"],
                    build_id=testrun.build_id,
                    environment_id=testrun.environment_id,
                ) for test_name, test_values in batch.items()
            ])

            # Attach known issues, if any
            for test in created_tests:
                metadata = metadata_names[test.metadata_id]
                test_full_name = join_name(metadata.suite, metadata.name)
                if test_full_name in issues.keys():
                    test.known_issues.add(*issues[test_full_name])

    except Exception as e:
        logger.error(f"CTS/VTS error: {e}")

    logger.info(f"Deleting PluginScratch with ID: {scratch.pk}")
    scratch.delete()
    return 0
