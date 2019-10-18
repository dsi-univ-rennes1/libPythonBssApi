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

def test_init_variables(test_config):
    global groupname, groupalias, accountname, autre_accountname, con
    con = create_connexion(test_config)
    groupname = "test_group_lib_python" + '@' + test_config['bss_domain']
    groupalias = "alias_test_group_lib_python" + '@' + test_config['bss_domain']
    accountname = "test_creation_lib_python" + '@' + test_config['bss_domain']
    autre_accountname = "autre_account_test_creation_lib_python" + '@' + test_config['bss_domain']

def test_cleanup_bss_environment(test_config):
    print("Cleanup BSS environment before running tests...")
    create_account(accountname)
    create_account(autre_accountname)
    delete_group(groupname)

def test_createGroup_cas_normal(test_config):
    newGroup = GroupService.createGroup(groupname)
    group = GroupService.getGroup(groupname)
    assert group.name == groupname


def test_createGroup_cas_groupeExistant(test_config):
    with pytest.raises(ServiceException):
        newGroup = GroupService.createGroup(groupname)

def test_getGroup_cas_normal(test_config):
    group = GroupService.getGroup(groupname)
    assert group.name == groupname

def test_getGroup_cas_groupe_inexistant(test_config):
    group = GroupService.getGroup("inexistant" + '@' + test_config['bss_domain'])
    assert group == None

def test_addGroupAliases_cas_Normal(test_config):
    GroupService.addGroupAliases(groupname, groupalias)
    group = GroupService.getGroup(groupname)
    assert groupalias in group.aliases

def test_addGroupAliases_cas_groupe_existant(test_config):
    with pytest.raises(ServiceException):
        GroupService.addGroupAliases(groupname, groupalias)

def test_updateGroupAliases_cas_Normal(test_config):
    GroupService.updateGroupAliases(groupname, "autre_alias_test_group_lib_python" + '@' + test_config['bss_domain'])
    group = GroupService.getGroup(groupname)
    assert ("autre_alias_test_group_lib_python" + '@' + test_config['bss_domain'] in group.aliases) and (groupalias not in group.aliases)

def test_removeGroupAliases_cas_Normal(test_config):
    GroupService.removeGroupAliases(groupname, "autre_alias_test_group_lib_python" + '@' + test_config['bss_domain'])
    group = GroupService.getGroup(groupname, full_info = True)
    assert "autre_alias_test_group_lib_python" + '@' + test_config['bss_domain'] not in group.aliases

def test_updateGroupAliases_cas_domaine_incorrect(test_config):
    with pytest.raises(ServiceException):
        GroupService.updateGroupAliases(groupname, "test_group_lib_python@mauvais.domaine.fr")

def test_removeGroupAliases_cas_alias_inconnu(test_config):
    with pytest.raises(ServiceException):
        GroupService.removeGroupAliases(groupname, "autre_alias_test_group_lib_python" + '@' + test_config['bss_domain'])

def test_addGroupMember_cas_Normal(test_config):
    GroupService.addGroupMembers(groupname, accountname)
    group = GroupService.getGroup(groupname)
    assert (accountname in group.members)

def test_updateGroupMembers_cas_Normal(test_config):
    GroupService.updateGroupMembers(groupname, autre_accountname)
    group = GroupService.getGroup(groupname)
    assert (autre_accountname in group.members) and (accountname not in group.members)

def test_removeGroupMembers_cas_Normal(test_config):
    GroupService.removeGroupMembers(groupname, autre_accountname)
    group = GroupService.getGroup(groupname)
    assert autre_accountname not in group.members

def test_removeGroupMembers_cas_alias_inconnu(test_config):
    with pytest.raises(ServiceException):
        GroupService.removeGroupMembers(groupname, autre_accountname)

def test_addGroupSenders_cas_Normal(test_config):
    GroupService.addGroupSenders(groupname, accountname)
    group = GroupService.getGroup(groupname, full_info = True)
    assert (accountname in group.senders)

def test_addGroupSenders_cas_compte_inconnu(test_config):
    with pytest.raises(NotFoundException):
        GroupService.addGroupSenders(groupname, "inexistant" + '@' + test_config['bss_domain'])

def test_updateGroupSenders_cas_Normal(test_config):
    GroupService.updateGroupSenders(groupname, autre_accountname)
    group = GroupService.getGroup(groupname, full_info = True)
    assert (autre_accountname in group.senders) and (accountname not in group.senders)

def test_removeGroupSenders_cas_Normal(test_config):
    GroupService.removeGroupSenders(groupname, autre_accountname)
    group = GroupService.getGroup(groupname)
    assert autre_accountname not in group.senders

def test_removeGroupSenders_cas_alias_inconnu(test_config):
    with pytest.raises(ServiceException):
        GroupService.removeGroupSenders(groupname, autre_accountname)

def test_deleteGroup_cas_normal(test_config):
    newGroup = GroupService.deleteGroup(groupname)
    group = GroupService.getGroup(groupname)
    assert group == None

def test_deleteGroup_cas_groupe_inexistant(test_config):
    with pytest.raises(ServiceException):
        newGroup = GroupService.deleteGroup(groupname)

