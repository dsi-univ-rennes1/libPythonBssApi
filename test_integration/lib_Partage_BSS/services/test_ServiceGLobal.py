import pytest
from lib_Partage_BSS.services import COSService
from lib_Partage_BSS.services import BSSConnexion
from lib_Partage_BSS.services import DomainService
import time as timer

def create_connexion(config):
    timer.sleep(1)
    con = BSSConnexion()
    if 'bss_url' in config:
        con.url = config['bss_url']
    con.setDomainKey({config['bss_domain']: config['bss_domain_key']})
    return BSSConnexion()

def test_init_variables(test_config):
    global con
    con = create_connexion(test_config)

def test_get_all_cos(test_config):
    global all_cos
    all_cos = COSService.getAllCOS(test_config['bss_domain'])
    assert len(all_cos) > 0

def test_get_cos(test_config):
    for one_cos in all_cos:
        cos = COSService.getCOS(test_config['bss_domain'], one_cos.name)
        assert cos.name == one_cos.name

def test_count_objects(test_config):
    count = DomainService.countObjects(test_config['bss_domain'], "userAccount")
    assert int(count) > 0

def test_get_domain(test_config):
    domain = DomainService.getDomain(test_config['bss_domain'])
    assert domain['name'] == test_config['bss_domain']

