# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from ..exceptions import (
    PaasResourceError,
)


def test_paas_resource_error():
    rid = 'xyz-1234-foo'
    exc = PaasResourceError(executor='test-docker',
                            action='run',
                            code=137,
                            resource_id=rid,
                            error_details="Container got SIGKILLed",
                            )

    # the args attribute is just because it is probably expected for
    # a subclass of RuntimeError
    assert exc.args == (rid, 'test-docker', 'run', 137)

    # details are more clearly available as other instance attributes
    assert exc.resource_id == rid
    assert exc.code == 137
