# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import pytest
import requests
import time
import toml

from ..exceptions import (
    GitLabUnavailableError,
    GitLabUnexpectedError,
    JobLaunchTimeout,
)
from ..job import JobHandle
from ..testing import (
    COORDINATOR_URL,
    COORDINATOR_JOB_REQUEST_URL,
    RunnerForTests,
    request_recorder,
    make_json_response,
    make_response,
)

COORDINATOR_JOB_BY_TOKEN_URL = COORDINATOR_URL + '/api/v4/job'

parametrize = pytest.mark.parametrize


@pytest.fixture
def runner():
    yield RunnerForTests(dict(executor='testing',
                              token='sesame-heptapod',
                              url=COORDINATOR_URL,
                              priv_foo='secret'))


def test_dump_inner_config(tmpdir, runner):
    dump_path = tmpdir / 'runner.toml'
    runner.dump_inner_config(dump_path)
    dumped = toml.loads(dump_path.read())
    assert dumped == dict(runners=[dict(executor='docker',
                                        url=COORDINATOR_URL,
                                        token='sesame-heptapod')
                                   ])


def test_request_job_got_one(monkeypatch, runner):
    records = []
    responses = [
        make_json_response(dict(id=1234), status_code=200),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    assert runner.request_job() == '{"id": 1234}'


@parametrize('http_code', (204, 409))
def test_request_job_none(monkeypatch, runner, http_code):
    records = []
    responses = [
        make_response(status_code=http_code, body=b''),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    assert runner.request_job() is None


def test_request_http_temp_error(monkeypatch, runner):
    records = []
    responses = [
        make_response(status_code=503, body=b'Come back later'),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    with pytest.raises(GitLabUnavailableError) as exc_info:
        runner.request_job()
    exc = exc_info.value
    assert exc.url == COORDINATOR_JOB_REQUEST_URL
    assert exc.message == 'Come back later'
    assert exc.status_code == 503


def test_request_http_hard_error(monkeypatch, runner):
    records = []
    responses = [
        make_response(status_code=404, body=b'Oops'),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    with pytest.raises(GitLabUnexpectedError) as exc_info:
        runner.request_job()
    exc = exc_info.value
    assert exc.url == COORDINATOR_JOB_REQUEST_URL
    assert exc.message == 'Oops'
    assert exc.status_code == 404


def test_request_connection_error(monkeypatch, runner):
    records = []
    responses = [
        requests.exceptions.ConnectionError("Mocking connection failure"),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    with pytest.raises(GitLabUnavailableError) as exc_info:
        runner.request_job()
    exc = exc_info.value
    assert exc.url == COORDINATOR_JOB_REQUEST_URL
    assert exc.message == "Mocking connection failure"
    assert exc.status_code is None


def test_is_job_finished(monkeypatch, runner):
    job_handle = JobHandle(runner_name=runner.unique_name,
                           job_id=1234,
                           token='job-token')
    records = []
    responses = [
        make_json_response(dict(id=1234, status='running'), status_code=200),
        make_json_response(dict(message='You are not authorized'),
                           status_code=401),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    assert runner.is_job_finished(job_handle) is False
    assert runner.is_job_finished(job_handle) is True


def test_is_job_finished_errors(monkeypatch, runner):
    job_handle = JobHandle(runner_name=runner.unique_name,
                           job_id=1234,
                           token='job-token')
    records = []
    responses = [
        make_response(status_code=418, body=b"I'm a teapot"),
        requests.exceptions.ConnectionError("Mocking connection failure"),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    with pytest.raises(GitLabUnexpectedError) as exc_info:
        runner.is_job_finished(job_handle)
    exc = exc_info.value
    assert exc.url == COORDINATOR_JOB_BY_TOKEN_URL
    assert exc.message == "I'm a teapot"
    assert exc.status_code == 418

    with pytest.raises(GitLabUnavailableError) as exc_info:
        runner.is_job_finished(job_handle)
    exc = exc_info.value
    assert exc.url == COORDINATOR_JOB_BY_TOKEN_URL
    assert exc.message == "Mocking connection failure"
    assert exc.status_code is None


def test_report_coordinator_job_failed(monkeypatch, runner):
    job_handle = JobHandle(runner_name=runner.unique_name,
                           job_id=74,
                           token='job-token')
    records = []
    responses = [
        make_json_response(dict(), status_code=200),
        make_json_response(dict(), status_code=200),
        make_json_response(dict(message='Forbidden'), status_code=403),
        make_json_response(dict(message='403 Forbidden - Job is not running'),
                           status_code=403),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    # known failure_reason (this example hurts)
    runner.report_coordinator_job_failed(job_handle, 'runner_unsupported')
    # unknown failure_reason (reporting not aware there's a close list)
    runner.report_coordinator_job_failed(job_handle,
                                         'paas runner failed to launch')
    assert records[0][:2] == ('put', 'https://gitlab.test/api/v4/jobs/74')
    with pytest.raises(GitLabUnexpectedError):
        runner.report_coordinator_job_failed(job_handle,
                                             'paas runner failed to launch')

    # No error if coordinator already knows the job is not running
    runner.report_coordinator_job_failed(job_handle, 'unknown_failure')
    assert records[-1][:2] == ('put', 'https://gitlab.test/api/v4/jobs/74')


def test_gl_job_send_trace(runner, monkeypatch):
    handle = JobHandle(runner_name=runner.unique_name,
                       job_id=74,
                       token='job-token')
    records = []
    responses = [
        make_json_response(13, status_code=202, headers=dict(Range='0-13')),
        make_json_response(dict(message='Bogus'), status_code=416),
        make_json_response(dict(message='403 Forbidden - Job is not running'),
                           status_code=403),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    new_range = runner.gl_job_send_trace(handle, message='foo',
                                         content_range='0-3')
    assert new_range == '0-13'

    with pytest.raises(GitLabUnexpectedError) as exc_info:
        runner.gl_job_send_trace(handle, "won't work", content_range='0-1')
    assert exc_info.value.status_code == 416

    # Special 403 for job already running does not raise and returns None
    assert runner.gl_job_send_trace(handle, message='foo',
                                    content_range='13-16') is None


def fake_gl_job_send_trace(runner):
    traces = {}

    def gl_append(job_handle, message, content_range):
        if message == "trigger-return-None":
            return None

        start, end = [int(i) for i in content_range.split('-')]
        prev_trace = traces.get(job_handle, '')
        prev_len = len(prev_trace)
        new_len = prev_len + len(message)

        if start != prev_len or end != new_len:
            raise GitLabUnexpectedError(
                url='http://whatever.heptapod.test',
                status_code=416,
                params=None,
                message='wrong range',
                headers={'content-range': content_range},
            )
        traces[job_handle] = prev_trace + message
        return f'0-{new_len}'

    runner.gl_job_send_trace = gl_append
    runner.get_trace = lambda jh: traces.get(jh)


def test_job_append_trace(runner):
    fake_gl_job_send_trace(runner)

    handle = JobHandle(runner_name=runner.unique_name,
                       job_id=65,
                       token='job-65-token')

    runner.job_append_trace(handle, "end-user info\n")
    assert runner.get_trace(handle) == "end-user info\n"

    runner.job_append_trace(handle, "final\n")
    assert runner.get_trace(handle) == "end-user info\nfinal\n"

    # special case where gl_job_send_trace returns None (happens
    # normally on jobs already not running)
    offset = handle.trace_offset
    runner.job_append_trace(handle, "trigger-return-None")
    assert handle.trace_offset == offset

    handle.trace_offset = 3  # bogus value
    with pytest.raises(GitLabUnexpectedError) as exc_info:
        runner.job_append_trace(handle, "won't work")
    assert exc_info.value.status_code == 416


def patch_gl_job_get_trace(runner, results, records):
    results = iter(results)

    def get_trace(project_id, job_id, token):
        records.append((project_id, job_id, token))

        result = next(results)
        if isinstance(result, str):
            return result
        else:
            raise result

    runner.gl_job_get_trace = get_trace


def test_job_wait_trace_no_token(runner):
    # this early return doesn't need valid arguments
    assert runner.job_wait_trace(None, None, None) is True


def test_job_wait_trace(runner):
    watch_token = 'watch-token'
    runner.config['paas_job_trace_watch'] = dict(token=watch_token,
                                                 timeout_seconds=0.1,
                                                 poll_step=0.01)

    project_id = 22
    job_id = 26
    job_handle = JobHandle(runner_name=runner.unique_name,
                           job_id=job_id,
                           token='job-26-token')
    get_trace_expected_args = (project_id, job_id, watch_token)

    def normal_sleep(amount):
        time.sleep(amount)
        return False

    def interrupted_sleep(amount):
        return True

    records = []
    patch_gl_job_get_trace(runner, ('', 'some log line'), records)
    assert runner.job_wait_trace(project_id, job_handle, normal_sleep)
    assert records == [get_trace_expected_args] * 2

    records = []
    # calling two times would give StopIteration
    patch_gl_job_get_trace(runner, ('', ), records)
    assert not runner.job_wait_trace(project_id, job_handle, interrupted_sleep)
    assert records == [get_trace_expected_args] * 1

    runner.config['paas_job_trace_watch']['timeout_seconds'] = 0.02
    # more than enough empty traces:
    patch_gl_job_get_trace(runner, ('', '', '', '', ''), records)
    with pytest.raises(JobLaunchTimeout) as exc_info:
        runner.job_wait_trace(project_id, job_handle, normal_sleep)

    assert exc_info.value.args == (job_handle, 0.02)
    # number of requests could be 1, 2 or 3

    # exception in HTTP call
    exc = GitLabUnexpectedError(url='https://some.trace.test',
                                status_code=428,
                                params=None,
                                message='buy me the coffee upgrade!',
                                )

    patch_gl_job_get_trace(runner, (exc, ), records)
    with pytest.raises(GitLabUnexpectedError) as exc_info:
        runner.job_wait_trace(project_id, job_handle, normal_sleep)
    assert exc_info.value.args == exc.args


def test_gl_job_get_trace(runner, monkeypatch):
    # using wait_trace to also test inner API consistency
    records = []
    responses = [
        make_response(status_code=502, body=b'backend not available'),
        make_response(status_code=200, body=b''),
        make_response(status_code=200, body=b'hello from inner runner'),

        make_response(status_code=403, body=b'surprise!'),
    ]

    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    watch_token = 'watch-token'
    runner.config['paas_job_trace_watch'] = dict(token=watch_token,
                                                 timeout_seconds=0.1,
                                                 poll_step=0.01)
    project_id = 23
    job_id = 27
    job_handle = JobHandle(runner_name=runner.unique_name,
                           job_id=job_id,
                           token='job-27-token')
    trace_url = ('https://gitlab.test/api/v4/projects'
                 f'/{project_id}/jobs/{job_id}/trace')
    expected_request = ('get', trace_url,
                        {'headers': {'Private-Token': 'watch-token'},
                         'params': None
                         })

    assert runner.job_wait_trace(project_id, job_handle, time.sleep)
    assert records == [expected_request] * 3

    with pytest.raises(GitLabUnexpectedError) as exc_info:
        runner.job_wait_trace(project_id, job_handle, time.sleep)
    exc = exc_info.value
    assert exc.url == trace_url
    assert exc.status_code == 403
    assert exc.message == 'surprise!'


def test_job_handle_dump_load(runner):
    runner.paas_credentials = 'paascred1'
    job_handle = JobHandle(runner_name=runner.unique_name,
                           job_id=89,
                           token='job-89-token')
    restored = JobHandle.load(runner, job_handle.dump())
    assert restored == job_handle  # does not involve token
    assert restored.token == job_handle.token

    paas_resource = runner.paas_resource(38)
    assert paas_resource.credentials == 'paascred1'  # test assumption
    job_handle.paas_resource = paas_resource

    runner.paas_credentials = 'paascred2'
    restored = JobHandle.load(runner, job_handle.dump())
    assert restored == job_handle
    assert restored.token == job_handle.token
    assert restored.paas_resource.id == 38
    assert restored.paas_resource.credentials == 'paascred2'
