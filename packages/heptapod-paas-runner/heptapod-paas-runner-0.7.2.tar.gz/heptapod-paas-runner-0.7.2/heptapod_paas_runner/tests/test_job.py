# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from ..job import (
    JobHandle,
    all_job_variables,
)


def test_job_handle_eq_hash():
    jh1 = JobHandle(runner_name='runner1',
                    job_id=1,
                    token='should-be-unique')
    jh2 = JobHandle(runner_name='runner1',
                    job_id=2,
                    token='tok2')
    jh1_other_runner = JobHandle(runner_name='runner2',
                                 job_id=1,
                                 token='tok2')
    jh1_bis = JobHandle(runner_name='runner1',
                        job_id=1,
                        token='should-be-unique')

    assert jh1 == jh1
    assert jh1 != jh2
    assert jh1 != jh1_other_runner

    # set operations, thanks to JobHandle being hashable
    assert jh2 in {jh1, jh2}
    assert {jh1, jh1} == {jh1}
    assert len({jh1, jh2}) == 2
    assert len({jh1, jh1_other_runner}) == 2

    # token doesn't matter for equality and hash
    assert jh1 == jh1_bis
    assert len({jh1, jh1_bis}) == 1


def test_all_job_variables():
    job_data = dict(variables=[
        dict(key='CI_PIPELINE_ID', value="123", public=True, masked=False),
        dict(key='W3!RD-ch$rs', value="foo", public=False, masked=False),
    ])
    assert all_job_variables(job_data) == {
        'CI_PIPELINE_ID': '123',
        'W3!RD-ch$rs': 'foo'
    }
