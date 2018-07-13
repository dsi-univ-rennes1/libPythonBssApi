import pytest

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

@pytest.fixture
def test_config(request):
    config = {}
    config['bss_domain'] = request.config.getoption("--bss_domain")[0]
    config['bss_domain_key'] = request.config.getoption("--bss_domain_key")[0]
    if request.config.getoption("--bss_url"):
        config['bss_url'] = request.config.getoption("--bss_url")[0]
    return config

