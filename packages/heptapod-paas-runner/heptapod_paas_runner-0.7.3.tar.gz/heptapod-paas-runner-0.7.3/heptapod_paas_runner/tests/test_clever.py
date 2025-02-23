# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import json
import pytest
import requests
import time
import toml

from .. import clever
from ..clever import (
    CC_ORGA_ID_ATTRIBUTE,
    CC_ORGA_TOKEN_ATTRIBUTE,
    DEFAULT_FLAVOR,
    FLAVOR_JOB_VARIABLE_NAME,
    CleverCloudDockerRunner,
    CleverCloudFlavor,
    CleverCloudOrganization,
    OrganizationNotFound,
    CleverCloudApplication,
)
from ..docker import DockerBuildHelper
from ..exceptions import (
    DeploymentBranchAlreadyExisting,
    PaasProvisioningError,
    PaasResourceError,
)
from ..testing import (
    COORDINATOR_URL,
    request_recorder,
    make_json_response,
    make_response,
)

HEPTAPOD_TOKEN = 'Cl3vr1234'
CC_ORGA_ID = 'orga_some_uuid'
CC_TOKEN = 'clever-orga-deploying-token'

parametrize = pytest.mark.parametrize
API_ERROR_KINDS = ['parseable', 'unparseable', 'standard-fields']
FLAVOR_M = CleverCloudFlavor(dict(name='reference-m',
                                  mem=8192,
                                  cpus=4))
FLAVOR_S = CleverCloudFlavor(dict(name='reference-m',
                                  mem=4096,
                                  cpus=2))


def make_runner(**kwargs):
    return CleverCloudDockerRunner(dict(executor='clever-docker',
                                        token=HEPTAPOD_TOKEN,
                                        cc_orga_id=CC_ORGA_ID,
                                        cc_token=CC_TOKEN,
                                        url=COORDINATOR_URL,
                                        **kwargs))


@pytest.fixture
def runner():
    yield make_runner()


@pytest.fixture
def multi_tenant_runner():
    yield make_runner(cc_multi_tenant=True)


def test_config_methods(tmpdir, runner):
    dump_path = tmpdir / 'runner.toml'
    runner.dump_inner_config(dump_path)
    dumped = toml.loads(dump_path.read())
    # Clever Cloud creds must not be propagated
    assert dumped == dict(runners=[dict(executor='docker',
                                        url=COORDINATOR_URL,
                                        token=HEPTAPOD_TOKEN,
                                        )
                                   ])


def test_flavor_weight_bias():
    # just to avoid not having any assertion on this, and avoiding
    # obvious buggy values such as 0 or 1
    assert FLAVOR_M.weight >= 8
    assert repr(FLAVOR_M) == (
        "CleverCloudFlavor({'name': 'reference-m', 'mem': 8192, 'cpus': 4})"
    )

    flavor_4xl = CleverCloudFlavor(dict(name='test-4xl',
                                        mem=FLAVOR_M.ram_mib * 16,
                                        cpus=4))
    # asserting the effect of the bias, not the (float) actual values.
    assert flavor_4xl.weight == 32 * FLAVOR_M.weight


def test_min_requestable_weight(runner, monkeypatch):
    # testing first runner.provision()
    records = []
    responses = [
        # available flavors for Heptapod Runner variant
        make_json_response([dict(name='jenkins-runner-XL',
                                 mem=65536,
                                 available=True),
                            dict(name='heptapod-runner-S',
                                 mem=4096,
                                 cpus=2,
                                 available=True),
                            dict(name='heptapod-runner-M',
                                 mem=8192,
                                 cpus=4,
                                 available=True),
                            dict(name='heptapod-runner-4XL',
                                 mem=65536,
                                 cpus=16,
                                 available=False),
                            ]),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    assert runner.min_requestable_weight == FLAVOR_M.weight

    runner.cc_max_flavor = 'S'
    assert runner.min_requestable_weight == FLAVOR_S.weight


@parametrize('extra_env', ['no-extra-env', 'extra-env'])
@parametrize('multi_tenant', ['multi_tenant', 'fixed_cc_orga'])
def test_provision_launch(runner, extra_env, multi_tenant, monkeypatch):
    if extra_env == 'extra-env':
        runner.config['cc_extra_env'] = {'CC_EXTRA': "some clever option"}
    is_multi_tenant = multi_tenant == 'multi_tenant'

    # testing first runner.provision()
    records = []
    responses = [
        # instance type query (for expected weight)
        make_json_response([dict(name='UnrelatedApplication',
                                 version='20220202'),
                            dict(name='Docker',
                                 flavors=[dict(name=DEFAULT_FLAVOR,
                                               available=True)],
                                 version='20210101'),
                            ]),
        # available flavors for Heptapod Runner variant
        make_json_response([dict(name='jenkins-runner-XL', available=True),
                            dict(name='heptapod-runner-M',
                                 mem=8192,
                                 cpus=4,
                                 available=True),
                            dict(name='heptapod-runner-4XL', available=False),
                            ]),
        # instance type query (for app creation)
        make_json_response([dict(name='UnrelatedApplication',
                                 version='20220202'),
                            dict(name='Docker',
                                 flavors=[dict(name=DEFAULT_FLAVOR,
                                               available=True)],
                                 version='20210101'),
                            ]),
        # app creation
        make_json_response(
            dict(id='some-uuid',
                 deployment=dict(httpUrl='https://clever.test/app-git-repo'),
                 instance=dict(maxFlavor=dict(name='heptapod-runner-M',
                                              cpus=4,
                                              mem=8192),
                               ),
                 )),
        # environment variable setting TODO QUESTION Clever:
        #   don't know actual expected status code, might be 204
        make_json_response(dict(), status_code=200),

        # waits for Git repo to be ready
        make_json_response(
            dict(id='some-uuid',
                 deployment=dict(repoState='CREATED'),
                 )),
        make_json_response(
            dict(id='some-uuid',
                 deployment=dict(repoState='CREATED'),
                 )),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    if is_multi_tenant:
        runner.fixed_cc_orga = None
        # attributes request to GitLab
        responses.insert(3, make_json_response([
            dict(key=CC_ORGA_ID_ATTRIBUTE, value='orga-id-from-attr'),
            dict(key=CC_ORGA_TOKEN_ATTRIBUTE, value='orga-token-from-attr'),
            ]))

    job = dict(id=777,
               variables=[
                   dict(key='CI_PROJECT_ROOT_NAMESPACE', value='tenant'),
                   ])
    assert runner.expected_weight(job) == FLAVOR_M.weight

    resource = runner.provision(job)
    assert isinstance(resource, CleverCloudApplication)
    assert resource.app_id == 'some-uuid'
    assert resource.weight == FLAVOR_M.weight
    # covering log_fmt(), without exact assertion (wording may change)
    assert 'launched=False' in resource.log_fmt()

    if is_multi_tenant:
        assert len(records) == 6
        gl_attr_req = records[3]
        meth, url, attr_kwargs = gl_attr_req
        assert meth.lower() == 'get'
        assert url == ('https://gitlab.test/api/v4'
                       '/groups/tenant/custom_attributes')
        assert attr_kwargs['headers'] == {'Private-Token': 'Cl3vr1234'}
        provision_req, put_env_req = records[4:]
        cc_orga_id = 'orga-id-from-attr'
        cc_token = 'orga-token-from-attr'
    else:
        assert len(records) == 5
        provision_req, put_env_req = records[3:]
        cc_orga_id = 'orga_some_uuid'
        cc_token = 'clever-orga-deploying-token'

    meth, url, prov_kwargs = provision_req
    assert meth.lower() == 'post'
    assert url == ('https://api.clever-cloud.com/v2'
                   '/organisations/%s/applications' % cc_orga_id)
    prov_data = prov_kwargs['json']
    assert prov_data['name'] == 'hpd-job-Cl3vr123-777'
    assert prov_data['instanceVersion'] == '20210101'
    assert prov_data['zone'] == 'par'
    assert prov_data['minFlavor'] == 'heptapod-runner-M'
    assert prov_data['maxFlavor'] == 'heptapod-runner-M'

    meth, url, env_kwargs = put_env_req
    assert meth.lower() == 'put'
    sent_env = env_kwargs['json']

    # this one is really necessary
    assert sent_env['CC_MOUNT_DOCKER_SOCKET'] == 'true'

    if extra_env == 'extra-env':
        assert sent_env['CC_EXTRA'] == 'some clever option'

    # now testing runner.launch()

    git_push_records = []  # list mostly for easy mutability

    def fake_git_push(helper, url):
        if git_push_records:
            raise DeploymentBranchAlreadyExisting(url, 'branch')
        git_push_records.append(url)

    monkeypatch.setattr(DockerBuildHelper, 'git_push', fake_git_push)
    runner.launch(resource, job)
    assert git_push_records == [
        'https://Jenkins:%s@clever.test/app-git-repo' % cc_token,
        ]
    assert 'launched=True' in resource.log_fmt()

    # idempotency: relaunching can happen in case there is a bug in
    # state tracking (currently the case) or in rare cases where a
    # hard shutdown happened right after the push.
    runner.launch(resource, job)
    assert len(git_push_records) == 1


def test_wait_deployability(runner, monkeypatch):
    records = []
    responses = [
        # direct error cases
        make_json_response(dict(details='wildly unexpected response schema')),
        make_json_response(
            dict(id=4004,  # actually seen if resource doesn't exist
                 type='error',
                 message='no such app'),
            status_code=404),
        # successful case
        make_json_response(dict(deployment=dict(repoState='CREATED'))),
        # two pending response to actually sleep in the loop
        make_json_response(dict(deployment=dict(repoState='CREATING'))),
        make_json_response(dict(deployment=dict(repoState='CREATING'))),
    ]

    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    app = CleverCloudApplication(orga=runner.fixed_cc_orga,
                                 app_id='app_234',
                                 deploy_url='https://cc.test/app_234',
                                 user='git',
                                 password='git')
    with pytest.raises(PaasResourceError) as exc_info:
        runner.wait_deployability(app)
    assert exc_info.value.code == 3

    with pytest.raises(PaasResourceError) as exc_info:
        runner.wait_deployability(app)
    exc = exc_info.value
    assert exc.code == 4004
    assert exc.transport_code == 404

    runner.deployment_repo_wait_step = 0.01
    # make sure to timeout at least on second request
    runner.deployment_repo_timeout = 0.015

    runner.wait_deployability(app)

    with pytest.raises(PaasResourceError) as exc_info:
        runner.wait_deployability(app)
    assert exc_info.value.code == 4


def test_decommission(runner, monkeypatch):
    records = []
    responses = [
        make_json_response(
            dict(id=302,  # actually seen
                 message='deleted',
                 type='success',
                 )),
        make_json_response(
            dict(id=4004,  # actually seen if resource doesn't exist
                 type='error',
                 message='no such app'),
            status_code=404),
        make_json_response(
            dict(id=5001,
                 type='error',
                 message='crash'),
            status_code=500),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    resource = CleverCloudApplication(orga=runner.fixed_cc_orga,
                                      app_id='app_234',
                                      deploy_url='https://cc.test/app_234',
                                      user='git',
                                      password='git')
    assert runner.decommission(resource)
    # resource is supposed not to exist any more,
    # this is consistent with next fake HTTP response
    assert not runner.decommission(resource)

    with pytest.raises(PaasResourceError) as exc_info:
        runner.decommission(resource)
    exc = exc_info.value
    assert exc.action == 'delete'
    assert exc.resource_id == 'app_234'
    assert exc.transport_code == 500
    assert exc.code == 5001


@parametrize('multi_tenant', ['multi_tenant', 'fixed_cc_orga'])
def test_decommission_all(runner, multi_tenant, monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda duration: None)
    is_multi_tenant = multi_tenant == 'multi_tenant'
    decom_kwargs = {}

    records = []
    responses = [
        # list of applications
        make_json_response([
            dict(name='hpd-job-%s-48' % runner.unique_name,
                 id='cc-app-1',
                 instance=dict(maxFlavor=dict(name='heptapod-runner-M',
                                              cpus=4,
                                              mem=8192)
                               ),
                 deployment=dict(httpUrl='https://cc.test/app/1')),
            dict(name='hpd-job-otherrunner-49',
                 instance=dict(flavors=[dict(name='heptapod-runner-S',
                                             cpus=2,
                                             mem=4096)
                                        ]),
                 id='cc-app-2',
                 deployment=dict(httpUrl='https://cc.test/app/2')),
            dict(name='unrelated application!',
                 id='cc-app-3',
                 deployment=dict(httpUrl='https://cc.test/app/3')),
        ]),
        make_json_response(
            dict(id=302,
                 message='deleted',
                 type='success',
                 )),
    ]
    if is_multi_tenant:
        responses.insert(0, make_json_response([
            dict(key=CC_ORGA_ID_ATTRIBUTE, value='orga-id-from-attr'),
            dict(key=CC_ORGA_TOKEN_ATTRIBUTE, value='orga-token-from-attr'),
            ]))
        runner.fixed_cc_orga = None
        decom_kwargs['gitlab_namespace'] = 'some-ns'

    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    assert runner.decommission_all(**decom_kwargs) == (1, 2)


def test_decommission_all_errors(runner, monkeypatch):
    # without an orga id if runner doesn't have a fixed orga
    runner.fixed_cc_orga = None
    with pytest.raises(ValueError) as exc_info:
        runner.decommission_all()

    # assertion just to make sure it's not another cause of ValueError
    assert runner.unique_name in exc_info.value.args[0]

    # with a namespace, without a fixed orga on the runner
    # when reading of orga creds is incomplete
    runner.gitlab_custom_attributes = lambda ns, atts, **kw: {}
    with pytest.raises(PaasProvisioningError) as exc_info:
        runner.decommission_all(gitlab_namespace='some-ns')


@parametrize('response_kind', API_ERROR_KINDS)
def test_provision_error(runner, monkeypatch, response_kind):
    if response_kind == 'standard-fields':
        # this is an actual error got due to missing version in early
        # experiments, so that's maybe one we might later not to trigger
        # a raise. Meanwhile it is kept here for further reference.
        error_response = make_json_response(
            dict(
                id=9017,
                message='The specified instance does not exist',
                type='error',
            ),
            status_code=400)
    elif response_kind == 'parseable':
        error_response = make_json_response(dict(msg="not your day"),
                                            status_code=404)
    else:
        error_response = make_response(500, b'not even JSON')

    records = []
    responses = [
        # instance type query
        make_json_response([dict(name='Docker',
                                 flavors=[dict(name=DEFAULT_FLAVOR,
                                               available=True)],
                                 version='20210101'),
                            ]),
        # available flavors for Heptapod Runner variant
        make_json_response([dict(name='jenkins-runner-XL', available=True),
                            dict(name='heptapod-runner-M',
                                 mem=1024,
                                 cpus=1,
                                 available=True),
                            ]),
        # app creation
        error_response,
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    with pytest.raises(PaasProvisioningError) as exc_info:
        runner.provision(dict(id=123))

    exc = exc_info.value
    assert exc.executor == 'clever-docker'
    assert exc.action == 'create-app'
    if response_kind == 'standard-fields':
        assert exc.transport_code == 400
        # can change once we get more info on Clever API
        assert exc.code == 9017
        assert exc.error_details == 'The specified instance does not exist'
        # just asserting it's the req_data dict:
        assert exc.action_details['instanceType'] == 'docker'
    elif response_kind == 'parseable':
        assert exc.transport_code == 404
        assert exc.error_details == json.dumps(dict(msg='not your day'))
    else:
        assert exc.transport_code == 500
        assert exc.error_details == "not even JSON"


@parametrize('response_kind', API_ERROR_KINDS)
def test_get_available_flavors_error(runner, monkeypatch, response_kind):
    if response_kind == 'standard-fields':
        error_response = make_json_response(
            dict(
                id=9782,
                message='This error message and its id are fictive)',
                type='error',
            ),
            status_code=400)
    elif response_kind == 'parseable':
        error_response = make_json_response(dict(msg="not your day"),
                                            status_code=404)
    else:
        error_response = make_response(500, b'not even JSON')

    records = []
    monkeypatch.setattr(clever, 'CC_API_RETRY_DELAY_SECONDS', 0)
    responses = [
        # instance type query
        make_json_response([dict(name='Docker',
                                 flavors=[dict(name=DEFAULT_FLAVOR,
                                               available=True)],
                                 version='20210101'),
                            ]),
        # app creation
        error_response,
        error_response,
        error_response,
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    with pytest.raises(PaasProvisioningError) as exc_info:
        runner.provision(dict(id=123))

    exc = exc_info.value
    assert exc.executor == 'clever-docker'
    assert exc.action == 'get-available-flavors'
    if response_kind == 'standard-fields':
        assert exc.transport_code == 400
        # can change once we get more info on Clever API
        assert exc.code == 9782
        assert 'are fictive' in exc.error_details
        # just asserting it's the req_data dict:
        assert exc.action_details['context'] == 'heptapod-runner'
    elif response_kind == 'parseable':
        assert exc.transport_code == 404
        assert exc.error_details == json.dumps(dict(msg='not your day'))
    else:
        assert exc.transport_code == 500
        assert exc.error_details == "not even JSON"


@parametrize('response_kind', API_ERROR_KINDS)
def test_cc_docker_instance_type_error(runner, monkeypatch, response_kind):
    records = []
    if response_kind == 'standard-fields':
        error_response = make_json_response(
            dict(id=3857,
                 type='error',
                 message='getting instances failed'),
            status_code=400)
    elif response_kind == 'parseable':
        error_response = make_json_response(
            dict(msg='Unexpected error payload'),
            status_code=400)
    else:
        error_response = make_response(500, b'not even JSON')
    monkeypatch.setattr(clever, 'CC_API_RETRY_DELAY_SECONDS', 0)
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, [error_response] * 3))

    with pytest.raises(PaasProvisioningError) as exc_info:
        runner.cc_docker_instance_type()
    exc = exc_info.value

    if response_kind == 'standard-fields':
        assert exc.transport_code == 400
        assert exc.code == 3857
        assert exc.error_details == 'getting instances failed'
    elif response_kind == 'parseable':
        assert exc.transport_code == 400
        assert exc.error_details == json.dumps(
            dict(msg='Unexpected error payload'))
    else:
        assert exc.transport_code == 500
        assert exc.error_details == "not even JSON"


@parametrize('response_kind', API_ERROR_KINDS)
def test_cc_put_env_error(runner, monkeypatch, response_kind):
    records = []
    if response_kind == 'standard-fields':
        error_response = make_json_response(
            dict(id=273,
                 type='error',
                 message='putting env failed'),
            status_code=400)
    elif response_kind == 'parseable':
        error_response = make_json_response(
            dict(msg='I said no'),
            status_code=400)
    else:
        error_response = make_response(500, b'not even JSON')
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, [error_response]))

    app = CleverCloudApplication(orga=runner.fixed_cc_orga,
                                 app_id='clever-app-uuid',
                                 deploy_url='http://somwhere.test',
                                 user=None,
                                 password=None,
                                 )
    with pytest.raises(PaasResourceError) as exc_info:
        app.put_env({'CC_MY_ENVIRON': 'something'})

    exc = exc_info.value

    if response_kind == 'standard-fields':
        assert exc.resource_id == 'clever-app-uuid'
        assert exc.code == 273
        assert exc.transport_code == 400
        assert exc.error_details == 'putting env failed'
    elif response_kind == 'parseable':
        assert exc.code is None
        assert exc.transport_code == 400
        assert exc.error_details == json.dumps(dict(msg='I said no'))
    else:
        assert exc.code is None
        assert exc.transport_code == 500
        assert exc.error_details == "not even JSON"


def test_config_flavour():
    conf_default = '3XL'
    assert DEFAULT_FLAVOR != conf_default  # avoid tautological test

    runner = make_runner(cc_default_flavor=conf_default)
    assert runner.cc_default_flavor == conf_default


def test_cc_select_flavor(runner):
    instance_type = dict(type='docker',
                         flavors=[
                             dict(name='nano', available=False),
                             dict(name='M', available=True),
                             dict(name='XL', available=True),
                             ])

    def do_select(flavor):
        """Just a shortcut."""
        job = {}
        if flavor is not None:
            job['variables'] = [dict(key=FLAVOR_JOB_VARIABLE_NAME,
                                     value=flavor),
                                ]
        return runner.cc_select_flavor(instance_type, job)

    # default from Runner config
    assert do_select(None).api_name == 'heptapod-runner-M'

    assert do_select('XL').api_name == 'heptapod-runner-XL'

    runner.cc_max_flavor = 'M'  # making XL oversized (error code 2)

    for unavailable, error_code in (('nano', 1),
                                    ('not-a-flavor', 1),
                                    ('XL', 2),
                                    ):
        with pytest.raises(PaasProvisioningError) as exc_info:
            do_select(unavailable)

        exc = exc_info.value
        assert exc.action == 'check-flavor'
        assert exc.code == error_code
        assert exc.executor == 'clever-docker'


def test_cc_app_dump_load(runner):
    # for an application dumped before GitLab namespace was tracked
    resource = CleverCloudApplication(orga=runner.fixed_cc_orga,
                                      app_id='app_234',
                                      deploy_url='https://cc.test/app_234',
                                      user='git',
                                      password='git')
    orga = runner.fixed_cc_orga
    orga.token = 'updated-token'
    orga.git_user = 'heptapod'

    restored = runner.load_paas_resource(resource.dump())
    assert restored.app_id == resource.app_id
    assert restored.deploy_url == resource.deploy_url
    assert restored.git_push_url == (
        'https://heptapod:updated-token@cc.test/app_234')


def test_cc_app_orga_restoration_failure(multi_tenant_runner):
    runner = multi_tenant_runner
    initial_orga = CleverCloudOrganization(orga_id='some-uuid',
                                           gitlab_namespace='glns',
                                           token='hush',
                                           git_user='git',
                                           base_api_url='http://api.test',
                                           )
    resource = CleverCloudApplication(orga=initial_orga,
                                      app_id='app_234',
                                      deploy_url='https://cc.test/app_234',
                                      user='git',
                                      password='git')
    dumped = resource.dump()

    # now the runner goes multi-tenant
    # …but retrieval of the organization corresponding to namespace fails

    def failing_cc_orga(*a, **kw):
        raise PaasProvisioningError(executor=runner.executor,
                                    action='find-orga',
                                    code=404)

    runner.cc_orga = failing_cc_orga

    restored = runner.load_paas_resource(dumped)
    assert restored.orga == OrganizationNotFound(initial_orga.gitlab_namespace)

    # not much can be done on the restored resource, but at least
    # it can be dumped again, for perhaps better luck after a restart
    assert restored.dump() == dumped

    with pytest.raises(PaasResourceError) as exc_info:
        runner.decommission(restored)
    assert exc_info.value.code == 22


def test_job_cc_orga_fixed(runner):
    # case of the default fixed orga (job payload doesn't matter)
    orga = runner.job_cc_orga(None)
    assert orga is not None
    assert orga.orga_id == CC_ORGA_ID


def test_job_cc_orga_not_fixed_errors(multi_tenant_runner, monkeypatch):
    runner = multi_tenant_runner

    records = []
    responses = [
        make_json_response([]),
        make_response(404, b'unknown namespace (not even JSON)'),
    ]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))

    with pytest.raises(PaasProvisioningError) as exc_info:
        runner.cc_orga(gitlab_namespace='foo')
    assert exc_info.value.action == 'find-orga'

    with pytest.raises(PaasProvisioningError) as exc_info:
        runner.job_cc_orga(dict(id=123,
                                variables=[dict(
                                    key='CI_PROJECT_ROOT_NAMESPACE',
                                    value='foo'),
                                ]))
    assert exc_info.value.action == 'find-orga'
