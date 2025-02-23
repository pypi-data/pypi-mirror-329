# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import pytest
import subprocess
import toml

from ..local_docker import (
    LocalDockerRunner,
    LocalDockerApplication,
)
from ..docker import DockerBuildHelper
from ..exceptions import (
    PaasResourceError,
)
from ..testing import (
    COORDINATOR_URL,
)


@pytest.fixture
def runner():
    yield LocalDockerRunner(dict(executor='local-docker',
                                 token='sesame-heptapod',
                                 url=COORDINATOR_URL))


def test_config_methods(tmpdir, runner):
    dump_path = tmpdir / 'runner.toml'
    runner.dump_inner_config(dump_path)
    dumped = toml.loads(dump_path.read())
    assert dumped == dict(runners=[dict(executor='docker',
                                        url=COORDINATOR_URL,
                                        token='sesame-heptapod')
                                   ])


def test_docker_socket():
    min_conf = dict(executor='local-docker',
                    token='sesame-heptapod',
                    url=COORDINATOR_URL)
    config = min_conf.copy()
    config['host'] = 'unix:///some/path.socket'
    runner = LocalDockerRunner(config)
    assert runner.docker_socket == '/some/path.socket'

    config = min_conf.copy()
    config['host'] = 'https://docker.test'
    with pytest.raises(ValueError) as exc_info:
        LocalDockerRunner(config)
    msg = exc_info.value.args[0]
    assert 'only Unix' in msg

    # full defaulting
    runner = LocalDockerRunner(min_conf)
    assert runner.docker_socket == '/var/run/docker.sock'


def test_provision(runner):
    resource = runner.provision(dict(id=76))
    assert isinstance(resource, LocalDockerApplication)
    # full name not much meaningful to test
    assert resource.app_id.endswith('-76')


def test_launch_error(runner, monkeypatch):

    def raise_error(helper, runner, *a):
        raise RuntimeError('oops', *a)

    monkeypatch.setattr(DockerBuildHelper, 'write_build_context', raise_error)
    resource = runner.provision(dict(id=123))
    with pytest.raises(PaasResourceError) as exc_info:
        runner.launch(resource, '{"id": null}')

    exc = exc_info.value
    assert exc.executor == 'local-docker'
    assert exc.resource_id == resource.app_id
    assert exc.error_details == '''RuntimeError('oops', '{"id": null}')'''


def subprocess_recorder(monkeypatch, records, exit_codes):

    def call(*a, **kw):
        records.append((a, kw))
        exit_code = exit_codes[0]
        exit_codes[:] = exit_codes[1:]
        return exit_code

    def check_call(*a, **kw):
        code = call(*a, **kw)
        if code != 0:
            raise subprocess.CalledProcessError(
                "Command %r returned non-zero exit status %d", a, code)

    monkeypatch.setattr(subprocess, 'call', call)
    monkeypatch.setattr(subprocess, 'check_call', check_call)


def test_launch_decommission(runner, monkeypatch):
    # again a test for our own self-consistency, does not involve docker at all
    records = []
    subprocess_recorder(monkeypatch, records, [0, 0, 0])

    job_data = dict(id=123)
    resource = runner.provision(job_data)
    runner.launch(resource, job_data)
    runner.decommission(resource)
    assert [rec[0][0][:2] for rec in records] == [
        ('docker', 'build'),
        ('docker', 'run'),
        ('docker', 'rmi'),
    ]


def test_launch_docker_error(runner, monkeypatch):
    # again a test for our own self-consistency, does not involve docker at all
    records = []
    subprocess_recorder(monkeypatch, records, [0, 1])

    job_data = dict(id=123)
    resource = runner.provision(job_data)
    with pytest.raises(PaasResourceError) as exc_info:
        runner.launch(resource, job_data)

    exc = exc_info.value
    assert exc.executor == 'local-docker'
    assert exc.resource_id == resource.app_id
    assert exc.error_details.startswith('CalledProcessError')

    assert [rec[0][0][:2] for rec in records] == [
        ('docker', 'build'),
        ('docker', 'run'),
    ]


def test_paas_resource_dump_load(runner):
    resource = LocalDockerApplication('app_234')

    restored = runner.load_paas_resource(resource.dump())
    assert restored.app_id == resource.app_id
