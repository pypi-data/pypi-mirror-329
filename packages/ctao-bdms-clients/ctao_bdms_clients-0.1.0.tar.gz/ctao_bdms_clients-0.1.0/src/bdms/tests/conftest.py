import os
import subprocess as sp
from datetime import datetime
from secrets import token_hex

import pytest
from rucio.client.scopeclient import ScopeClient

USER_CERT = os.getenv("RUCIO_CFG_CLIENT_CERT", "/opt/rucio/etc/usercert.pem")
USER_KEY = os.getenv("RUCIO_CFG_CLIENT_KEY", "/opt/rucio/etc/userkey.pem")


@pytest.fixture(scope="session")
def test_user():
    return "root"


@pytest.fixture(scope="session")
def _auth_proxy(tmp_path_factory):
    """Auth proxy needed for accessing RSEs"""
    # Key has to have 0o600 permissions, but due to the way we
    # we create and mount it, it does not. We copy to a tmp file
    # set correct permissions and then create the proxy
    sp.run(
        [
            "voms-proxy-init",
            "-valid",
            "9999:00",
            "-cert",
            USER_CERT,
            "-key",
            USER_KEY,
        ],
        check=True,
    )


@pytest.fixture(scope="session")
def test_vo():
    return "ctao.dpps.test"


@pytest.fixture(scope="session")
def test_scope(test_user):
    """To avoid name conflicts and old state, use a unique scope for the tests"""
    # length of scope is limited to 25 characters
    random_hash = token_hex(2)
    date_str = f"{datetime.now():%Y%m%d_%H%M%S}"
    scope = f"t_{date_str}_{random_hash}"

    sc = ScopeClient()
    sc.add_scope(test_user, scope)
    return scope
