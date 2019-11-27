import pytest
from lib_Partage_BSS.models.Group import Group
from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS.exceptions.NotFoundException import NotFoundException
from lib_Partage_BSS.services import AccountService, GroupService, BSSConnexion
import time as timer


def create_account(name):
    account = AccountService.getAccount(name)
    if account == None:
        AccountService.createAccount(name,"{ssha}BIDON")

def delete_group(name):
    group = GroupService.getGroup(name)
    if group != None:
        GroupService.deleteGroup(name)

def create_connexion(config):
    timer.sleep(1)
    con = BSSConnexion()
    if 'bss_url' in config:
        con.url = config['bss_url']
    con.setDomainKey({config['bss_domain']: config['bss_domain_key']})
    return BSSConnexion()

def test_cleanup_bss_environment(test_config):
    print("Cleanup BSS environment before running tests...")
    create_account(test_config['accountname'])
    create_account(test_config['autre_accountname'])
    delete_group(test_config['groupname'])

def test_createGroup_cas_normal(test_config):
    newGroup = GroupService.createGroup(test_config['groupname'])
    group = GroupService.getGroup(test_config['groupname'])
    assert group.name == test_config['groupname']


def test_createGroup_cas_groupeExistant(test_config):
    with pytest.raises(ServiceException):
        newGroup = GroupService.createGroup(test_config['groupname'])

def test_getGroup_cas_normal(test_config):
    group = GroupService.getGroup(test_config['groupname'])
    assert group.name == test_config['groupname']

def test_getGroup_cas_groupe_inexistant(test_config):
    group = GroupService.getGroup("inexistant" + '@' + test_config['bss_domain'])
    assert group == None

def test_addGroupAliases_cas_Normal(test_config):
    GroupService.addGroupAliases(test_config['groupname'], test_config['groupalias'])
    group = GroupService.getGroup(test_config['groupname'])
    assert test_config['groupalias'] in group.aliases

def test_addGroupAliases_cas_groupe_existant(test_config):
    with pytest.raises(ServiceException):
        GroupService.addGroupAliases(test_config['groupname'], test_config['groupalias'])

def test_updateGroupAliases_cas_Normal(test_config):
    GroupService.updateGroupAliases(test_config['groupname'], test_config['autre_groupalias'])
    group = GroupService.getGroup(test_config['groupname'])
    assert (test_config['autre_groupalias'] in group.aliases) and (test_config['groupalias'] not in group.aliases)

def test_removeGroupAliases_cas_Normal(test_config):
    GroupService.removeGroupAliases(test_config['groupname'], test_config['autre_groupalias'])
    group = GroupService.getGroup(test_config['groupname'], full_info = True)
    assert test_config['autre_groupalias'] not in group.aliases

def test_updateGroupAliases_cas_domaine_incorrect(test_config):
    with pytest.raises(ServiceException):
        GroupService.updateGroupAliases(test_config['groupname'], "test_group_lib_python@mauvais.domaine.fr")

def test_removeGroupAliases_cas_alias_inconnu(test_config):
    with pytest.raises(ServiceException):
        GroupService.removeGroupAliases(test_config['groupname'], test_config['autre_groupalias'])

def test_addGroupMember_cas_Normal(test_config):
    GroupService.addGroupMembers(test_config['groupname'], test_config['accountname'])
    group = GroupService.getGroup(test_config['groupname'])
    assert (test_config['accountname'] in group.members)

def test_updateGroupMembers_cas_Normal(test_config):
    GroupService.updateGroupMembers(test_config['groupname'], test_config['autre_accountname'])
    group = GroupService.getGroup(test_config['groupname'])
    assert (test_config['autre_accountname'] in group.members) and (test_config['accountname'] not in group.members)

def test_removeGroupMembers_cas_Normal(test_config):
    GroupService.removeGroupMembers(test_config['groupname'], test_config['autre_accountname'])
    group = GroupService.getGroup(test_config['groupname'])
    assert test_config['autre_accountname'] not in group.members

def test_removeGroupMembers_cas_alias_inconnu(test_config):
    with pytest.raises(ServiceException):
        GroupService.removeGroupMembers(test_config['groupname'], test_config['autre_accountname'])

def test_addGroupSenders_cas_Normal(test_config):
    GroupService.addGroupSenders(test_config['groupname'], test_config['accountname'])
    group = GroupService.getGroup(test_config['groupname'], full_info = True)
    assert (test_config['accountname'] in group.senders)

def test_addGroupSenders_cas_compte_inconnu(test_config):
    with pytest.raises(NotFoundException):
        GroupService.addGroupSenders(test_config['groupname'], "inexistant" + '@' + test_config['bss_domain'])

def test_updateGroupSenders_cas_Normal(test_config):
    GroupService.updateGroupSenders(test_config['groupname'], test_config['autre_accountname'])
    group = GroupService.getGroup(test_config['groupname'], full_info = True)
    assert (test_config['autre_accountname'] in group.senders) and (test_config['accountname'] not in group.senders)

def test_removeGroupSenders_cas_Normal(test_config):
    GroupService.removeGroupSenders(test_config['groupname'], test_config['autre_accountname'])
    group = GroupService.getGroup(test_config['groupname'])
    assert test_config['autre_accountname'] not in group.senders

def test_removeGroupSenders_cas_alias_inconnu(test_config):
    with pytest.raises(ServiceException):
        GroupService.removeGroupSenders(test_config['groupname'], test_config['autre_accountname'])

def test_deleteGroup_cas_normal(test_config):
    newGroup = GroupService.deleteGroup(test_config['groupname'])
    group = GroupService.getGroup(test_config['groupname'])
    assert group == None

def test_deleteGroup_cas_groupe_inexistant(test_config):
    with pytest.raises(ServiceException):
        newGroup = GroupService.deleteGroup(test_config['groupname'])

