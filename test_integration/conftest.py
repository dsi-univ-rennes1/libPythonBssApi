import pytest
from lib_Partage_BSS.services import BSSConnexion
import time as timer

def pytest_addoption(parser):
    parser.addoption("--bss_domain", action="append", default=[],
        help="Domaine pour tests API BSS")

    parser.addoption("--bss_domain_key", action="append", default=[],
        help="Clé de domaine pour tests API BSS")

    parser.addoption("--bss_url", action="append", default=[],
        help="URL accès API BSS")

# def pytest_generate_tests(metafunc):
#     if 'bss_domain' in metafunc.fixturenames:
#         metafunc.parametrize("bss_domain",
#                              metafunc.config.getoption('bss_domain'))

def create_connexion(config):
    timer.sleep(1)
    con = BSSConnexion()
    if 'bss_url' in config:
        con.url = config['bss_url']
    con.setDomainKey({config['bss_domain']: config['bss_domain_key']})
    return BSSConnexion()

@pytest.fixture(scope="session")
def test_config(request):
    config = {}
    config['bss_domain'] = request.config.getoption("--bss_domain")[0]
    config['bss_domain_key'] = request.config.getoption("--bss_domain_key")[0]
    if request.config.getoption("--bss_url"):
        config['bss_url'] = request.config.getoption("--bss_url")[0]

    con = create_connexion(config)

    config['accountname'] = "test_creation_lib_python" + '@' + config['bss_domain']
    config['accountalias'] = "alias_" + config['accountname']
    config['autre_accountname'] = "autre_account_test_creation_lib_python" + '@' + config['bss_domain']
    config['autre_accountalias'] = "alias_" + config['autre_accountname']
    config['groupname'] = "test_group_lib_python" + '@' + config['bss_domain']
    config['groupalias'] = "alias_test_group_lib_python" + '@' + config['bss_domain']
    config['autre_groupalias'] = "autre_alias_test_group_lib_python" + '@' + config['bss_domain']
    config['resourcename'] = "test_resource_lib_python" + '@' + config['bss_domain']
    config['userPassword']="{SSHA}94S7kyTEEfkS5YMwL0YMhgkjKuPJQWEm"
    config['zimbraCalResType']="Location"
    config['displayName']="Test"

    return config

