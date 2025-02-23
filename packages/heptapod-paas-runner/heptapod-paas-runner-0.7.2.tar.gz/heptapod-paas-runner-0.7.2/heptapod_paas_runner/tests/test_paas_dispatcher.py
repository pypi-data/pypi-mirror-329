# Copyright 2021-2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import json
from overrides import overrides
import signal
import threading
import time

import pytest

from ..testing import RunnerForTests
from ..exceptions import (
    GitLabUnavailableError,
    GitLabUnexpectedError,
    JobLaunchTimeout,
    PaasProvisioningError,
    PaasResourceError,
)
from .. job import JobHandle
from ..paas_dispatcher import (
    JobEventType,
    PaasDispatcher,
    main as dispatcher_main,
)

parametrize = pytest.mark.parametrize


class ApplicationForTests:
    """Mock application object, just storing details for assertions.
    """
    def __init__(self, runner_name, job_id, paas_secret, weight=1):
        self.runner_name = runner_name
        self.job_id = job_id
        self.app_id = 'app_%s_%d' % (runner_name, job_id)
        self.paas_secret = paas_secret
        self.weight = weight
        self.launched = False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.app_id)

    def dump(self):
        return dict(runner_name=self.runner_name,
                    weight=self.weight,
                    job_id=self.job_id)

    def log_fmt(self):
        return repr(self)


class FlavorForTests:
    """Mock Flavor object, with just enough info for assertions."""
    def __init__(self, weight):
        self.weight = weight


class Runner(RunnerForTests):

    executor = 'paas-test-docker'

    paas_secret = None
    """Model for an additional secret used with the PAAS API."""

    weighted = False
    """If True, job weight is set in place."""

    weight_requestable = False
    """If True, the runner is able to request jobs with a maximum weight."""

    def __init__(self, config):
        super(Runner, self).__init__(config)
        self.acquirable_jobs = []
        self.acquired_jobs = {}
        self.launched_jobs_resources = []
        self.progress_errors = {}  # used to trigger errors in job progress
        self.coord_reported_failed = []
        self.failing_decommissions = []
        self.successful_decommissions = []
        self.job_requests_count = 0
        self.job_traces = {}
        self.available_flavors = {'L': FlavorForTests(weight=4),
                                  'M': FlavorForTests(weight=2),
                                  }

    def request_job(self, max_weight=None):
        self.job_requests_count += 1
        if not self.acquirable_jobs:
            return None

        if max_weight is None or not self.weighted:
            job = self.acquirable_jobs[0]
        else:
            for job in self.acquirable_jobs:
                if job['weight'] <= max_weight:
                    break
            else:
                return None

        self.acquirable_jobs.remove(job)
        job_id = job['id']
        job.setdefault('job_info', {}).setdefault('project_id', 1049)
        self.acquired_jobs[job_id] = job
        return json.dumps(job)

    def expected_weight(self, job):
        if self.weighted:
            return job['weight']
        else:
            # covers default impl for Runners without weight handling
            return super(Runner, self).expected_weight(job)

    def provision(self, job):
        job_id = job['id']
        success = self.acquired_jobs[job_id]['provision_ok']
        if success:
            return ApplicationForTests(self.unique_name, job_id,
                                       self.paas_secret,
                                       weight=job.get('weight', 1),
                                       )

        else:
            raise PaasProvisioningError(executor=self.executor,
                                        action='test-provision',
                                        code=321, transport_code=400,
                                        error_details="Read the doc!")

    def launch(self, app, job_data):
        job = self.acquired_jobs[app.job_id]
        print("Launching job %r" % job)
        if not job['launch_ok']:
            if job.get('exc_kind') == 'unexpected':
                raise RuntimeError("did not see that coming")
            else:
                raise PaasResourceError(executor=self.executor,
                                        action='test-plaunch',
                                        resource_id='cloud51',
                                        code=196, transport_code=400,
                                        error_details="Famous last words")

        self.launched_jobs_resources.append((app, job_data))
        job['status'] = 'launched'

    def job_wait_trace(self, project_id, job_handle, interruptible_sleep):
        job_details = self.acquired_jobs[job_handle.job_id]
        print("job_wait_trace for %s, details=%r" % (job_handle, job_details))
        calls = job_details.get('wait_trace_calls', 0) + 1
        job_details['wait_trace_calls'] = calls

        call_nr, response = job_details.get('wait_trace_response',
                                            (1, 'success'))
        if calls >= call_nr:
            if response == 'success':
                return True
            if response == 'timeout':
                raise JobLaunchTimeout(
                    job_handle,
                    job_details.get('wait_trace_timeout_value', 10))

        return False  # interruption

    def is_job_finished(self, job_handle):
        job_id = job_handle.job_id
        error = self.progress_errors.get(job_id)
        if error:
            raise error
        else:
            return self.acquired_jobs[job_id]['status'] == 'finished'

    def job_append_trace(self, job_handle, message):
        self.job_traces.setdefault(job_handle, []).append(message)
        job_handle.trace_offset += len(message)

    def report_coordinator_job_failed(self, job_handle, reason):
        self.coord_reported_failed.append((job_handle, reason))

    def mark_job_finished(self, job_id):
        self.acquired_jobs[job_id]['status'] = 'finished'

    def decommission(self, paas_resource):
        rsc_id = paas_resource.app_id
        if rsc_id in self.failing_decommissions:
            raise PaasResourceError(rsc_id, self.executor,
                                    action='decom', code=1)
        self.successful_decommissions.append(rsc_id)

    @overrides
    def load_paas_resource(self, data):
        return ApplicationForTests(paas_secret=self.paas_secret, **data)


Runner.register()


class WeightedRunner(Runner):
    executor = 'paas-test-weighted'


WeightedRunner.register()


def make_job_handle(runner, job_id, token,
                    expected_weight=1,
                    actual_weight=1,
                    with_resource=True):
    handle = JobHandle(runner.unique_name, job_id, token,
                       expected_weight=expected_weight)
    if with_resource:
        handle.paas_resource = ApplicationForTests(runner.unique_name,
                                                   job_id,
                                                   runner.paas_secret,
                                                   weight=actual_weight,
                                                   )

    return handle


DEFAULT_QUOTA_CONFIG = dict(reference_runner='testrunner',
                            reference_flavor='L',
                            reference_jobs_count=3,
                            )
"""Used when it doesn't matter much.

Tests about the quota would typically force it anyway.
Needs obviously a runner with human-readable name 'testrunner'.
"""


@pytest.fixture
def paas_dispatcher():
    dispatcher = PaasDispatcher(
        config=dict(
            concurrent=5,
            check_interval=0.01,
            job_progress_poll_interval=0.02,
            quota_computation=DEFAULT_QUOTA_CONFIG,
            runners=[dict(executor=Runner.executor,
                          name='testrunner',
                          url='http://heptapod.test',
                          token='secret'),
                     ]
            ))
    dispatcher.start_event_processing_thread()
    yield dispatcher

    dispatcher.shutdown_required = True


@pytest.fixture
def single_runner_dispatcher(paas_dispatcher):
    assert len(paas_dispatcher.runners) == 1
    runner_name, runner = next(iter(paas_dispatcher.runners.items()))
    yield paas_dispatcher, runner, runner_name


def wait_until(condition, timeout=10, tick=0.1, do_assert=False):
    start = time.time()
    while not condition() and time.time() - start < timeout:
        time.sleep(tick)
    if do_assert:
        assert condition()


def test_decommission_bogus(single_runner_dispatcher):
    dispatcher, _, runner_name = single_runner_dispatcher
    handle = JobHandle(runner_name=runner_name, job_id=23, token='jt23')
    # doesn't make sense without a PAAS resource, yet no crash occurs
    dispatcher.decommission(handle)
    # and no event was sent (probability of a blocked put is very low)
    assert dispatcher.reporting_queue.empty()


@parametrize('tracked', ('tracked', 'untracked'))
def test_decommission_full(single_runner_dispatcher, tracked):
    dispatcher, _, runner_name = single_runner_dispatcher
    runner = dispatcher.runners[runner_name]
    handle = make_job_handle(runner, 87, token='jt87')
    if tracked == 'tracked':
        dispatcher.to_decommission.add(handle)
    dispatcher.decommission(handle)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)
    assert runner.successful_decommissions == [handle.paas_resource.app_id]


def test_one_cycle(single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True),
        dict(id=13, token='jobtok13', provision_ok=False),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=False),
        dict(id=15, token='jobtok15', provision_ok=True, launch_ok=True),
        dict(id=16, token='jobtok16', provision_ok=True,
             launch_ok=False, exc_kind='unexpected'),
    ))

    dispatcher.poll_all_launch()
    wait_until(lambda: dispatcher.total_job_launches >= 5)
    wait_until(lambda: len(dispatcher.launch_errors) >= 3)

    # reports about launch attempts can arrive in any order
    assert set(jh.full_id for jh in dispatcher.launch_errors) == {
        (runner_name, 13),
        (runner_name, 14),
        (runner_name, 16),
    }
    assert set(jh.full_id for jh in dispatcher.launched_jobs) == {
        (runner_name, 12),
        (runner_name, 15),
    }

    # testing runner has more details about jobs
    launched = runner.launched_jobs_resources
    assert len(launched) == 2
    assert set(job[0] for job in launched) == {
        ApplicationForTests(runner.unique_name, 12, None),
        ApplicationForTests(runner.unique_name, 15, None)
    }

    # cover debug log dumps
    dispatcher.log_state_signal(signal.SIGUSR1, None)


def test_failure_coordinator_report_failure(monkeypatch,
                                            single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    # no need to wait for good in tests
    from .. import paas_dispatcher
    monkeypatch.setattr(paas_dispatcher,
                        'COORDINATOR_REPORT_LAUNCH_FAILURES_RETRY_DELAY',
                        0.1)

    attempts = []

    def report_coordinator(*a, **kw):
        attempts.append((a, kw))
        raise RuntimeError("Failed to report failure to coordinator")

    runner.report_coordinator_job_failed = report_coordinator
    runner.acquirable_jobs.append(
        dict(id=17, token='jobtok17', provision_ok=False))

    dispatcher.poll_all_launch()
    wait_until(lambda: dispatcher.total_job_launches >= 1)

    # all exception were catched, we had the expected amount
    # of attempts at reporting to coordinator.
    assert len(attempts) == 3

    attempts.clear()
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)

    assert dispatcher.decommission_launch_failures
    assert dispatcher.potential_concurrency == 0
    assert dispatcher.potential_weight == 0


def test_launcher_thread_shutdown_between_retries(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    attempts = []

    def report_coordinator(*a, **kw):
        attempts.append((a, kw))
        raise RuntimeError("Failed to report failure to coordinator")

    runner.report_coordinator_job_failed = report_coordinator
    runner.acquirable_jobs.append(
        dict(id=18, token='jobtok18', provision_ok=False))

    dispatcher.poll_all_launch()

    # with the standard retry delay, we'll detect the first attempt way
    # before the first actual retry.
    wait_until(lambda: attempts)
    dispatcher.shutdown_signal(signal.SIGTERM, None)
    assert dispatcher.shutdown_required

    # take the opportunity to test shutdown-reentrance
    dispatcher.shutdown()

    assert len(dispatcher.pending_jobs) == 1
    job_handle = list(dispatcher.pending_jobs)[0]
    assert job_handle.job_id == 18

    queue = dispatcher.reporting_queue
    # the queue can be not empty (POLL_CYCLE_FINISHED actually seen to
    # be in there). Asserting that would make the test flaky.
    # This doesn't happen often, so we must exclude the loop from coverage.
    while not queue.empty():  # pragma: no cover
        msg = queue.get()
        assert msg != (job_handle, JobEventType.LAUNCH_FAILED)


def test_timed_out_job_trace_appending_failure(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    append_attempts = []

    def job_append_trace(*a, **kw):
        append_attempts.append((a, kw))
        raise RuntimeError("Failed to append to coordinator job trace")

    def job_wait_trace(project_id, job_handle, **kw):
        raise JobLaunchTimeout(job_handle, 1)

    runner.job_append_trace = job_append_trace
    runner.job_wait_trace = job_wait_trace

    pending_jh = make_job_handle(runner, 257, 'pj257',
                                 with_resource=True)
    pending_jh.paas_resource.launched = True
    pending_data = dict(id=pending_jh.job_id,
                        job_info=dict(project_id=383))

    dispatcher.pending_jobs[pending_jh] = pending_data
    dispatcher.potential_concurrency = 1
    dispatcher.potential_weight = pending_jh.paas_resource.weight

    dispatcher.launch_job(pending_jh, pending_data)
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)

    assert dispatcher.potential_concurrency == 0
    assert dispatcher.potential_weight == 0


def test_wait_job_trace_recovery(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher

    def job_wait_trace(project_id, job_handle, **kw):
        raise GitLabUnexpectedError(url='http://heptapod.example',
                                    status_code=415,
                                    params=None,
                                    message="Zombie job")

    runner.job_wait_trace = job_wait_trace

    pending_jh = make_job_handle(runner, 258, 'pj258',
                                 with_resource=True)
    pending_jh.paas_resource.launched = True
    pending_data = dict(id=pending_jh.job_id,
                        job_info=dict(project_id=383))

    dispatcher.pending_jobs[pending_jh] = pending_data
    dispatcher.potential_concurrency = 1
    dispatcher.potential_weight = pending_jh.paas_resource.weight

    dispatcher.launch_job(pending_jh, pending_data)
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)

    assert dispatcher.potential_concurrency == 0
    assert dispatcher.potential_weight == 0


def test_launch_progress_max_pending(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    dispatcher.max_pending_jobs = 2

    def pending_jobs():
        return set(jh.job_id for jh in dispatcher.pending_jobs)

    def launch_failures():
        return set(jh.job_id for jh in dispatcher.launch_errors)

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    def wait_trace_counts():
        return {job_id: details.get('wait_trace_calls', 0)
                for job_id, details in runner.acquired_jobs.items()
                }

    # wait_trace on the first two jobs gives an interruption,
    # which stops the launching thread, as if a general shutdown had
    # been signaled.
    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True,
             wait_trace_response=(2, 'success')),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True,
             wait_trace_response=(2, 'timeout')),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True),
    ))

    dispatcher.poll_all_launch()
    # the test depends on the fact that poll_all_launch() repolls a runner
    # immmediately if it gave a job unless limits are reached.
    wait_until(lambda: len(dispatcher.pending_jobs) >= 2
               and list(wait_trace_counts().values()) == [1, 1])
    assert runner.job_requests_count == 2
    assert pending_jobs() == {12, 13}
    # cover debug log dumps with pending jobs
    dispatcher.log_state_signal(signal.SIGUSR1, None)

    # provisioning has been called for the pending jobs, make sure it
    # won't be called again by adding an assertion in the provisioning method
    provision = runner.provision

    def no_reprovision(job_data):
        assert job_data['id'] not in (12, 13)
        return provision(job_data)

    runner.provision = no_reprovision

    # resuming as if loading state (TODO actually dump/load state?)
    # job 12 will launch successfully,
    # job 13 will have a trace timeout -> launch failure
    dispatcher.start_initial_threads()
    wait_until(lambda: len(pending_jobs()) == 0)
    assert launched_jobs() == {12}
    assert launch_failures() == {13}

    # polling again will launch job 14 successfully
    dispatcher.poll_all_launch()
    wait_until(lambda: len(dispatcher.launched_jobs) >= 2)
    assert launched_jobs() == {12, 14}


def test_jobs_progress_max_concurrency(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    dispatcher.max_concurrency = 2

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    def to_decommission_jobs():
        return set(jh.job_id for jh in dispatcher.to_decommission)

    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True),
    ))
    dispatcher.poll_all_launch()
    # the test depends on the fact that poll_all_launch() repolls a runner
    # immmediately if it gave a job unless max concurrency is reached.
    assert runner.job_requests_count == 2
    wait_until(lambda: dispatcher.total_job_launches >= 2)

    assert launched_jobs() == {12, 13}

    dispatcher.poll_launched_jobs_progress_once()
    assert launched_jobs() == {12, 13}

    runner.mark_job_finished(13)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: 13 not in launched_jobs())
    wait_until(lambda: 13 not in to_decommission_jobs())

    dispatcher.poll_all_launch()
    wait_until(lambda: dispatcher.total_job_launches >= 3)
    assert launched_jobs() == {12, 14}

    # covering decommissionning error while we're at it
    runner.failing_decommissions.append(
        ApplicationForTests(runner.unique_name, 12, None).app_id)
    runner.mark_job_finished(12)
    dispatcher.poll_launched_jobs_progress_once()

    wait_until(lambda: len(launched_jobs()) <= 1)
    assert launched_jobs() == {14}


def test_runner_by_human_name(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    assert dispatcher.runner_by_human_name('testrunner') is runner

    with pytest.raises(KeyError) as exc_info:
        dispatcher.runner_by_human_name('foo')

    assert exc_info.value.args == ('foo', )


def test_init_max_concurrency(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    dispatcher.init_max_concurrency(
        dict(quota_computation=DEFAULT_QUOTA_CONFIG,
             concurrent=25,
             ))
    assert dispatcher.max_concurrency == 25
    assert dispatcher.weighted_quota == 12


@parametrize('weight_requestable', ['requestable', 'non_requestable'])
def test_jobs_weighing(single_runner_dispatcher, weight_requestable):
    dispatcher, runner, _ = single_runner_dispatcher
    runner.weighted = True
    dispatcher.weighted_quota = 100
    dispatcher.max_concurrency = 10000  # infinite

    weight_requestable = runner.weight_requestable = (
        weight_requestable == 'requestable')

    runner.min_requestable_weight = 30 if weight_requestable else 80

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    def to_decommission_jobs():
        return set(jh.job_id for jh in dispatcher.to_decommission)

    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True,
             weight=50),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True,
             weight=60),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True,
             weight=30),
    ))

    def poll_assert_launched_jobs(expected):
        # the test depends on the fact that poll_all_launch() repolls a runner
        # immmediately if it gave a job unless max concurrency is reached.
        prev_requests = runner.job_requests_count
        prev_launches = dispatcher.total_job_launches
        expected_new = len(expected - launched_jobs())
        expected_total_launches = expected_new + prev_launches

        dispatcher.poll_all_launch()

        assert runner.job_requests_count == expected_new + prev_requests
        wait_until(
            lambda: dispatcher.total_job_launches >= expected_total_launches)

        assert launched_jobs() == expected

    # If the runner is able to request a small job, then it will take
    # job 14, otherwise the weight of job 12 is already too close to the
    # limit to take the risk of obtaining a job since it could weigh as much
    # as 80.
    poll_assert_launched_jobs({12, 14} if weight_requestable else {12})
    dispatcher.poll_launched_jobs_progress_once()

    runner.mark_job_finished(12)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: 12 not in launched_jobs())
    wait_until(lambda: 12 not in to_decommission_jobs())

    # In requestable case, 14 is already running, and we can request
    # a weight at most 70, which matches job 13.
    # In the non requestable case, the next to launch is 13, leaving
    # again not enough headroom for the potential weight of 80
    poll_assert_launched_jobs({13, 14} if weight_requestable else {13})

    # Note that in the requestable case, no further request has been
    # issued because we are at weight 90 and the minimal (requestable)
    # job weight is 30. Let's change that and retry.
    if weight_requestable:
        runner.min_requestable_weight = 5
        prev_req_count = runner.job_requests_count
        runner.acquirable_jobs.append(
            dict(id=15, token='jobtok15', provision_ok=True, launch_ok=True,
                 weight=20)
        )

        dispatcher.poll_all_launch()

        # there was a new request, but it found no suitable job
        assert runner.job_requests_count == prev_req_count + 1
        wait_until(lambda: dispatcher.reporting_queue.empty())
        assert 15 not in launched_jobs()


def test_jobs_progress_errors(single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    url = 'https://heptapod.test/api/v4/job'
    runner.progress_errors = {
        5: GitLabUnavailableError(message='Rebooting', url=url),
        6: GitLabUnexpectedError(message="I'm a teapot",
                                 status_code=418,
                                 params=None,
                                 url=url,
                                 ),
        7: RuntimeError("Something went baaad"),
        }

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    runner.acquirable_jobs.extend((
        dict(id=5, token='jobtok5', provision_ok=True, launch_ok=True),
        dict(id=6, token='jobtok6', provision_ok=True, launch_ok=True),
        dict(id=7, token='jobtok7', provision_ok=True, launch_ok=True),
    ))
    dispatcher.poll_all_launch()
    wait_until(lambda: len(launched_jobs()) >= 3, do_assert=True)

    dispatcher.poll_launched_jobs_progress_once()


def test_save_load_state(tmpdir):
    config = dict(
        state_file=str(tmpdir / 'paas-dispatcher.json'),
        quota_computation=DEFAULT_QUOTA_CONFIG,
        runners=[dict(executor=Runner.executor,
                      name='testrunner',
                      url='http://heptapod1.test',
                      token='secret1'),
                 dict(executor=Runner.executor,
                      name='testrunner2',
                      url='http://heptapod2.test',
                      token='secret2'),
                 ])
    dispatcher = PaasDispatcher(config=config)
    assert not dispatcher.state_file_path.exists()  # checking test assumption
    dispatcher.load_state()
    assert not dispatcher.launched_jobs

    runner1 = dispatcher.runners['secret1']
    runner2 = dispatcher.runners['secret2']
    runner1.paas_secret = 'before-save-load'

    launched_jobs = {
        make_job_handle(runner1, 956, 'job-token-1',
                        expected_weight=5,
                        actual_weight=17),
        # make sure the process does not fail if PAAS resource is missing
        # even though that should not happen for launched jobs!
        make_job_handle(runner2, 957, 'job-token-2',
                        expected_weight=13,
                        with_resource=False),
    }
    # since we don't have a running polling loop, the pending jobs
    # will stay inert.
    pending_job_handle = make_job_handle(runner1, 54, 'pendingtok1',
                                         actual_weight=10)
    pending_jobs = {pending_job_handle: dict(id=54,
                                             job_info=dict(project_id=383),
                                             ),
                    }

    dispatcher.launched_jobs = launched_jobs
    dispatcher.pending_jobs = pending_jobs
    dispatcher.save_state()
    assert dispatcher.state_file_path.exists()

    dispatcher = PaasDispatcher(config=config)
    assert not dispatcher.launched_jobs
    runner1 = dispatcher.runners['secret1']
    runner1.paas_secret = 'after-save-load'

    dispatcher.load_state()
    # quick assertion on runner_name and job_id
    assert dispatcher.launched_jobs == launched_jobs

    # job limits (notice how actual weight took precedence over
    # expected weight). The CleverApplications will use the just reloaded
    # flavors instead of serializing the weight.
    assert dispatcher.potential_concurrency == 3
    assert dispatcher.potential_weight == 40  # 17 + 13 + 10

    # details of job handles and PAAS resources
    handles_by_id = {jh.job_id: jh for jh in dispatcher.launched_jobs}
    jh1 = handles_by_id[956]
    rsc1 = jh1.paas_resource
    assert rsc1 is not None
    assert rsc1.paas_secret == 'after-save-load'

    assert handles_by_id[957].paas_resource is None

    # pending jobs
    assert dispatcher.pending_jobs == pending_jobs
    # telling the testing runner that provision/launch should work
    # for the pending job.
    runner1.acquired_jobs[54] = dict(provision_ok=True, launch_ok=True)

    dispatcher.start_initial_threads()
    dispatcher.start_event_processing_thread()
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    assert pending_job_handle in dispatcher.launched_jobs


def test_save_load_decommission_state(tmpdir):
    state_path = tmpdir / 'paas-dispatcher.json'
    config = dict(
        state_file=str(state_path),
        quota_computation=DEFAULT_QUOTA_CONFIG,
        runners=[dict(executor=Runner.executor,
                      name='testrunner',
                      url='http://heptapod1.test',
                      token='secret1'),
                 ])
    dispatcher = PaasDispatcher(config=config)
    assert not dispatcher.state_file_path.exists()  # checking test assumption

    # state file without decommission info
    with open(state_path, 'w') as statef:
        json.dump(dict(launched=[], pending=[]), statef)
    dispatcher.load_state()
    assert not dispatcher.to_decommission

    runner = dispatcher.runners['secret1']

    # since we don't have a running polling loop, the jobs to decommisson
    # will stay inert.
    to_decomm_jobs = {
        make_job_handle(runner, 736, 'job-token-1'),
        # make sure the process does not fail if PAAS resource is missing
        # even though that should not happen for launched jobs!
        make_job_handle(runner, 737, 'job-token-2', with_resource=False),
    }

    dispatcher.to_decommission = to_decomm_jobs
    assert not state_path.exists()
    dispatcher.save_state()
    assert state_path.exists()

    # New Dispatcher and Runner instances
    dispatcher = PaasDispatcher(config=config)
    runner = dispatcher.runners['secret1']
    assert not dispatcher.to_decommission

    dispatcher.load_state()
    # quick assertion on runner_name and job_id
    assert dispatcher.to_decommission == to_decomm_jobs

    # details of job handles and PAAS resources
    handles_by_id = {jh.job_id: jh for jh in dispatcher.to_decommission}
    jh1 = handles_by_id[736]
    rsc1 = jh1.paas_resource
    assert rsc1 is not None
    assert handles_by_id[737].paas_resource is None

    dispatcher.start_initial_threads()
    dispatcher.start_event_processing_thread()
    wait_until(lambda: len(dispatcher.to_decommission) < 2)

    # runner.decommission was called
    assert runner.successful_decommissions == [rsc1.app_id]
    # succesful decommission event sent and processed
    assert len(dispatcher.to_decommission) == 1
    assert dispatcher.to_decommission.pop().job_id == 737


@parametrize('saturation', ('concurrency', 'weight'))
def test_poll_loop(saturation):
    dispatcher = PaasDispatcher(dict(
        concurrent=17,
        check_interval=0.01,
        job_progress_poll_interval=0.02,
        quota_computation=DEFAULT_QUOTA_CONFIG,
        runners=[dict(executor=Runner.executor,
                      name='testrunner',
                      token='some-secret',
                      url='http://heptapod.test'
                      )
                 ]))

    cycles_done = dispatcher.poll_loop(max_cycles=2)
    assert cycles_done == 2

    if saturation == 'concurrency':
        dispatcher.potential_concurrency = 17
    elif saturation == 'weight':
        dispatcher.potential_weight = dispatcher.weighted_quota

    cycles_done = dispatcher.poll_loop(max_cycles=2)
    # we're still making cycles, even though new jobs won't be
    # requested.
    assert cycles_done == 2

    # Graceful shutdown. Running the loop in a separate thread for testing
    # purposes
    # TODO change the interruptible sleep step
    poll_thread = threading.Thread(target=lambda: dispatcher.poll_loop(),
                                   daemon=True)
    poll_thread.start()
    dispatcher.shutdown_required = True
    poll_thread.join(timeout=10)
    assert not poll_thread.is_alive()


def test_main(tmpdir, monkeypatch):
    config_path = tmpdir / 'runner.toml'
    state_file_path = tmpdir / 'paas_dispatcher_state.json'
    config_path.write_text('\n'.join((
        'concurrent = 17',
        'state_file = "%s"' % state_file_path,
        '',
        '[quota_computation]',
        '  reference_runner = "testrunner"',
        '  reference_flavor = "L"',
        '  reference_jobs_count = 5',
        '',
        '[[runners]]',
        '  executor = "%s"' % Runner.executor,
        '  name = "testrunner"',
        '  token = "toml-secret"',
        '  url = "http://heptapod.test"',
    )), 'ascii')
    dispatcher_main(
        raw_args=['--poll-interval', '0',
                  '--poll-cycles', '2',
                  '--job-progress-poll-interval', '0',
                  '--debug-signal',
                  str(config_path)])

    def raiser(dispatcher, *a, **kw):
        raise RuntimeError("panic, panic, panic!")

    monkeypatch.setattr(PaasDispatcher, 'poll_loop', raiser)
    assert dispatcher_main(raw_args=[str(config_path)]) == 1


def test_main_missing_quota_config(tmpdir):
    config_path = tmpdir / 'runner.toml'
    state_file_path = tmpdir / 'paas_dispatcher_state.json'
    config_path.write_text('\n'.join((
        'concurrent = 17',
        'state_file = "%s"' % state_file_path,
        '',
        '[[runners]]',
        '  executor = "%s"' % Runner.executor,
        '  name = "testrunner"',
        '  token = "toml-secret"',
        '  url = "http://heptapod.test"',
    )), 'ascii')
    assert dispatcher_main(raw_args=[str(config_path)]) == 2


def test_wait_threads_failure(paas_dispatcher):
    test_finished = False

    def long_wait():
        """Sleeping forever until the end of the test.

        Stopping at some point is still necessary!
        """
        while not test_finished:
            time.sleep(0.1)

    thread = threading.Thread(target=long_wait)
    thread.name = 'test-wait-threads-failure'
    paas_dispatcher.launched_jobs_progress_thread = thread
    thread.start()

    paas_dispatcher.shutdown_required = True
    paas_dispatcher.wait_all_threads(timeout=0.1)
    # we went through the error case, TODO assert on warning log.
    assert thread.is_alive()
    # TODO we don't have the means to make the event processing thread
    # stop if it is waiting for a message in the queue yet

    test_finished = True
    thread.join()
