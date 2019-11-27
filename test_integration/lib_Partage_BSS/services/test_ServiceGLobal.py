import pytest
from lib_Partage_BSS.services import COSService
from lib_Partage_BSS.services import DomainService



def test_get_all_cos(test_config):
    all_cos = COSService.getAllCOS(test_config['bss_domain'])
    assert len(all_cos) > 0

def test_get_cos(test_config):
    all_cos = COSService.getAllCOS(test_config['bss_domain'])
    for one_cos in all_cos:
        cos = COSService.getCOS(test_config['bss_domain'], one_cos.name)
        assert cos.name == one_cos.name

def test_count_objects(test_config):
    count = DomainService.countObjects(test_config['bss_domain'], "userAccount")
    assert int(count) > 0

def test_get_domain(test_config):
    domain = DomainService.getDomain(test_config['bss_domain'])
    assert domain['name'] == test_config['bss_domain']

