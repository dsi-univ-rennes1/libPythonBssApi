import pytest
import os,json
from lib_Partage_BSS.services import COSService
from lib_Partage_BSS.services import DomainService
from lib_Partage_BSS.exceptions.NotFoundException import NotFoundException



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

def test_definition(test_config):
    historyDefinition = DomainService.getHistoryDefinition(test_config['bss_domain'])
    DomainService.deleteDefinition(test_config['bss_domain'])

    with pytest.raises(NotFoundException):
        definition = DomainService.getDefinition(test_config['bss_domain'])

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/sample-mailinglists.json', 'r') as jsonFile:
        definition = json.load(jsonFile)
        DomainService.createDefinition(test_config['bss_domain'], json.dumps(definition))

    definition = DomainService.getDefinition(test_config['bss_domain'])
    assert definition != None

    newHistoryDefinition = DomainService.getHistoryDefinition(test_config['bss_domain'])
    assert len(newHistoryDefinition["definition"]) > len(historyDefinition["definition"])
