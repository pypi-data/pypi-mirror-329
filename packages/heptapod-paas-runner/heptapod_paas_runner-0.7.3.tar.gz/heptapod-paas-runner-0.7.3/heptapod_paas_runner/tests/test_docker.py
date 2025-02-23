# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from copy import deepcopy
import json
import subprocess
import toml

import pytest

from ..docker import DockerBuildHelper
from ..docker import split_docker_image_domain
from ..exceptions import (
    DeploymentBranchAlreadyExisting,
)
from ..testing import (
    RunnerForTests,
    COORDINATOR_URL,
)


def test_split_docker_image_domain():
    """Same as tests of reference implementation.

    Except that the test is for a higher level, public method than the
    one we implement.

    Reference: https://github.com/distribution/distribution/blob/1563384b69df9376389fe45ce949173a6383770a/reference/normalize_test.go#L130 (TestParseRepositoryInfo)
    """  # noqa long URL
    for test_case in (
            dict(to_parse=("docker.io/fooo/bar",
                           "fooo/bar",
                           "index.docker.io/fooo/bar",
                           ),
                 domain="docker.io",
                 remainder="fooo/bar"),
            dict(to_parse=("ubuntu",
                           "library/ubuntu",
                           "docker.io/library/ubuntu",
                           ),
                 domain="docker.io",
                 remainder="library/ubuntu",
                 ),
            dict(to_parse=("nonlibrary/ubuntu",
                           "docker.io/nonlibrary/ubuntu",
                           ),
                 domain="docker.io",
                 remainder="nonlibrary/ubuntu",
                 ),
            dict(to_parse=("other/library",
                           "docker.io/other/library",
                           ),
                 domain="docker.io",
                 remainder="other/library",
                 ),
            dict(to_parse=("127.0.0.1:8000/private/moonbase",
                           ),
                 domain="127.0.0.1:8000",
                 remainder="private/moonbase",
                 ),
            dict(to_parse=("127.0.0.1:8000/privatebase",
                           ),
                 domain="127.0.0.1:8000",
                 remainder="privatebase",
                 ),
            dict(to_parse=("example.com:8000/private/moonbase",
                           ),
                 domain="example.com:8000",
                 remainder="private/moonbase",
                 ),
            dict(to_parse=("ubuntu-12.04-base",
                           "docker.io/library/ubuntu-12.04-base",
                           "index.docker.io/library/ubuntu-12.04-base",
                           ),
                 domain="docker.io",
                 remainder="library/ubuntu-12.04-base",
                 ),
            dict(to_parse=("foo",
                           "docker.io/library/foo",
                           "docker.io/foo",
                           ),
                 domain="docker.io",
                 remainder="library/foo",
                 ),
            dict(to_parse=("library/foo/bar",
                           "docker.io/library/foo/bar",
                           ),
                 domain="docker.io",
                 remainder="library/foo/bar",
                 ),
            dict(to_parse=("store/foo/bar",
                           "docker.io/store/foo/bar",
                           ),
                 domain="docker.io",
                 remainder="store/foo/bar",
                 ),
            dict(to_parse=("Foo/bar",
                           ),
                 domain="Foo",
                 remainder="bar",
                 ),
            dict(to_parse=("FOO/bar",
                           ),
                 domain="FOO",
                 remainder="bar",
                 ),

            ):
        for name in test_case['to_parse']:
            assert split_docker_image_domain(name) == (test_case['domain'],
                                                       test_case['remainder'])


def test_docker_git(tmpdir):
    dst_repo = tmpdir / 'dst'
    subprocess.check_call(('git', 'init', '--bare', str(dst_repo)))
    context_dir = tmpdir / 'docker-context'
    context_dir.mkdir()
    build_helper = DockerBuildHelper(context_dir,
                                     git_process_env={},
                                     git_user_name='Test Git',
                                     git_user_email='testgit@heptapod.test')

    # test shouldn't rely on current default base image (prone to change)
    build_helper.base_image = "heptapod-runner"

    runner = RunnerForTests(dict(executor='testing',
                                 token='s3s4me-heptapod',
                                 url=COORDINATOR_URL,
                                 priv_foo='secret'))

    job_json = '{"id": 3497}'
    build_helper.write_build_context(runner, json.loads(job_json))
    build_helper.git_push(str(dst_repo))

    clone_path = tmpdir / 'clone'
    subprocess.check_call(('git', 'clone', str(dst_repo), str(clone_path)))

    assert (clone_path / 'job.json').read() == job_json
    assert toml.loads((clone_path / 'runner.toml').read()) == dict(
        runners=[dict(executor='docker',
                      url=COORDINATOR_URL,
                      token='s3s4me-heptapod')
                 ])
    # No point repeating the entire Dockerfile
    assert (clone_path / 'Dockerfile').readlines()[0] == (
        "FROM heptapod-runner\n")

    git_log = build_helper.git('log', '-n', '1').splitlines()
    author_line = next(li for li in git_log if li.startswith(b'Author'))
    assert author_line == b'Author: Test Git <testgit@heptapod.test>'

    # error case: remote branch already existing
    context_dir = tmpdir / 'docker-context2'
    context_dir.mkdir()
    (context_dir / 'foo').write('foo')  # anything to commit
    build_helper.path = context_dir

    with pytest.raises(DeploymentBranchAlreadyExisting):
        build_helper.git_push(dst_repo)


def test_docker_base_image(tmpdir):
    img = 'heptapod-runner:explicit_tag'
    runner = RunnerForTests(dict(executor='testing',
                                 heptapod_runner_main_image=img,
                                 token='s3s4me-heptapod',
                                 url=COORDINATOR_URL,
                                 priv_foo='secret'))

    build_helper = DockerBuildHelper.from_runner_config(tmpdir, runner.config)
    build_helper.write_build_context(
        runner,
        dict(id=6534, comment="this is the job data, yes"))

    # No point repeating the entire Dockerfile
    assert (tmpdir / 'Dockerfile').readlines()[0] == "FROM %s\n" % img

    # No unknown config is passed down to final runner
    passed_runner_conf = toml.load(tmpdir / 'runner.toml')['runners'][0]
    assert 'heptapod_runner_main_image' not in passed_runner_conf


def test_dependency_proxy():
    common_job_data = dict(id=123, variables=[])

    build_helper = DockerBuildHelper('/irrelevant/path')

    job_data = deepcopy(common_job_data)
    build_helper.amend_job(job_data)
    assert job_data == common_job_data

    common_job_data['variables'].append(dict(
        key='CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX',
        value='heptapod.example:443/group/dependency_proxy/containers',
    ))

    # no image, no services
    job_data = deepcopy(common_job_data)
    build_helper.amend_job(job_data)
    assert job_data == common_job_data

    # with image and no services
    job_data = deepcopy(common_job_data)
    job_data['image'] = dict(name='debian:bullseye')
    build_helper.amend_job(job_data)
    assert job_data['image'] == dict(
        name='heptapod.example:443/group/'
        'dependency_proxy/containers/library/debian:bullseye')

    # an image not from Docker Hub shouldn't be changed
    non_docker_hub_img = dict(
        name='registry.heptapod.net:443/group/proj:latest')
    job_data = deepcopy(common_job_data)
    job_data['image'] = non_docker_hub_img
    build_helper.amend_job(job_data)
    assert job_data['image'] == non_docker_hub_img

    # with an official service image on Docker Hub
    job_data = deepcopy(common_job_data)
    job_data['services'] = [dict(name='nginx:latest')]
    build_helper.amend_job(job_data)
    assert job_data['services'][0] == dict(
        name='heptapod.example:443/group/'
        'dependency_proxy/containers/library/nginx:latest',
        alias='nginx')

    # with a namespaced service image on Docker Hub
    job_data = deepcopy(common_job_data)
    job_data['services'] = [dict(name='heptapod/heptapod:latest')]
    build_helper.amend_job(job_data)
    assert job_data['services'][0] == dict(
        name='heptapod.example:443/group/'
        'dependency_proxy/containers/heptapod/heptapod:latest',
        alias='heptapod-heptapod')

    # with service and user alias, the alias is unchanged
    job_data['services'] = [dict(name='nginx:latest', alias='web')]
    build_helper.amend_job(job_data)
    assert job_data['services'][0] == dict(
        name='heptapod.example:443/group/'
        'dependency_proxy/containers/library/nginx:latest',
        alias='web')

    # with service not from Docker Hub, it shouldn't be changed
    job_data = deepcopy(common_job_data)
    job_data['services'] = [non_docker_hub_img]
    build_helper.amend_job(job_data)
    assert job_data['services'][0] == non_docker_hub_img

    # with unexpected service definition, it's just forwarded
    job_data = deepcopy(common_job_data)
    service = dict(some_key='foo')
    job_data['services'] = [service.copy()]
    build_helper.amend_job(job_data)
    assert job_data['services'] == [service]
