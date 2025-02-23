# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import pytest
import requests
import toml

from ..testing import (
    make_response,
    make_json_response,
    request_recorder,
)
from ..paas_register import (
    create_conf_file,
    main,
    positive_int,
    register,
    valid_executor,
    valid_input,
)


parametrize = pytest.mark.parametrize


def test_valid_input_converter(monkeypatch):
    def converter(s):
        if s == 'foo':
            raise TypeError("Foo")
        if s == 'bar':
            raise ValueError("Bar")
        return s.capitalize()

    assert valid_input("heptapod", converter=converter) == 'Heptapod'

    monkeypatch.setattr("builtins.input", lambda prompt: "not a foo")
    assert valid_input("foo", converter=converter) == 'Not a foo'

    monkeypatch.setattr("builtins.input", lambda prompt: "not a bar")
    assert valid_input("bar", converter=converter) == 'Not a bar'

    monkeypatch.setattr("builtins.input", lambda prompt: "some string")
    assert valid_input("") == 'some string'
    assert valid_input(None,
                       initial_message="This is an important setting",
                       prompt="Setting: ") == 'some string'


def test_positive_int():
    assert positive_int(67) == 67
    assert positive_int("43") == 43

    for inp in ("-1", -2, "0"):
        with pytest.raises(TypeError) as exc_info:
            positive_int(inp)
        msg = exc_info.value.args[0].lower()
        assert "not a positive integer" in msg
        assert repr(inp) in msg


def test_valid_executor():
    assert valid_executor('clever-docker') == 'clever-docker'
    with pytest.raises(ValueError) as exc_info:
        valid_executor('imaginary')
    msg = exc_info.value.args[0].lower()
    assert 'executor' in msg


def test_create_conf_file(tmpdir):
    path = tmpdir / 'conf.toml'
    create_conf_file(path,
                     concurrency=10,
                     state_file_path='/some/path.state')

    with open(path) as conffile:
        conf = toml.load(conffile)
    assert conf == dict(concurrent=10,
                        state_file='/some/path.state')


def test_register(tmpdir, monkeypatch):
    records = []
    responses = [make_json_response(dict(token='runtøk'))]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    conf_path = tmpdir / 'conf.toml'
    conf_path.ensure()
    runner_name = 'Clever Jogger'
    register(conf_path, runner_name=runner_name,
             coordinator_url='https://heptapod.test/',
             token='regs3creet',
             executor='clever-docker')

    assert len(records) == 1
    request = records[0]
    assert request[0] == 'post'
    assert request[1] == 'https://heptapod.test/api/v4/runners'
    assert request[2]['json'] == dict(
        info=dict(name=runner_name),
        description=runner_name,
        active=False,
        token='regs3creet')

    with conf_path.open() as conf_fobj:
        conf = toml.load(conf_fobj)

    assert conf == dict(runners=[dict(token='runtøk',
                                      executor='clever-docker',
                                      url='https://heptapod.test/',
                                      name=runner_name,
                                      )])


def test_register_error(tmpdir, monkeypatch):
    records = []
    responses = [make_response(400, b"garbage")]
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, responses))
    conf_path = tmpdir / 'conf.toml'
    conf_path.ensure()
    runner_name = 'Clever Jogger'
    with pytest.raises(RuntimeError) as exc_info:
        register(conf_path, runner_name=runner_name,
                 coordinator_url='https://heptapod.test/',
                 token='regs3creet',
                 executor='clever-docker')
    exc_args = exc_info.value.args
    assert exc_args[0] == 400
    assert exc_args[1] == 'garbage'


@parametrize('result', ('success', 'failure'))
def test_main(tmpdir, monkeypatch, result):
    records = []
    if result == 'success':
        response = make_json_response(dict(token='runtøk'))
    else:
        response = make_response(403, b"Wrong token")
    monkeypatch.setattr(requests.api, 'request',
                        request_recorder(records, [response]))

    conf_path = tmpdir / 'conf.toml'
    runner_name = 'Clever Jogger'
    exit_code = main(
        raw_args=[str(conf_path),
                  '--name', runner_name,
                  '--coordinator-url', 'https://heptapod.test/',
                  '--registration-token', 'regs3creet',
                  '--executor', 'clever-docker',
                  '--max-concurrency', '32',
                  '--state-file-path', '/run/dispatcher.toml',
                  ])

    assert len(records) == 1
    request = records[0]
    assert request[0] == 'post'
    assert request[1] == 'https://heptapod.test/api/v4/runners'
    assert request[2]['json'] == dict(
        info=dict(name=runner_name),
        description=runner_name,
        active=False,
        token='regs3creet')

    # the configuration file will always have been created
    with conf_path.open() as conf_fobj:
        conf = toml.load(conf_fobj)

    if result == 'success':
        assert exit_code == 0
        assert conf == dict(concurrent=32,
                            state_file='/run/dispatcher.toml',
                            runners=[dict(token='runtøk',
                                          executor='clever-docker',
                                          url='https://heptapod.test/',
                                          name=runner_name,
                                          )])
    else:
        assert exit_code == 1
        assert conf == dict(concurrent=32,
                            state_file='/run/dispatcher.toml')
