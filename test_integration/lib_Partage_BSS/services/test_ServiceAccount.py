import pytest
from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS.services import AccountService

def create_account(name):
    account = AccountService.getAccount(name)
    if account == None:
        AccountService.createAccount(name,"{ssha}BIDON")

def delete_account(name):
    account = AccountService.getAccount(name)
    if account != None:
        AccountService.deleteAccount(name)

def test_cleanup_bss_environment(test_config):
    print("Cleanup BSS environment before running tests...")
    delete_account(test_config['accountname'])
    delete_account(test_config['autre_accountname'])

def test_createAccount_cas_normal(test_config):
    AccountService.createAccount(test_config['accountname'], "{ssha}BIDON")
    account = AccountService.getAccount(test_config['accountname'])
    assert account.name == test_config['accountname']

def test_createAccount_cas_compteExistant(test_config):
    with pytest.raises(ServiceException):
        AccountService.createAccount(test_config['accountname'], "{ssha}BIDON")

def test_getAccount_cas_normal(test_config):
    account = AccountService.getAccount(test_config['accountname'])
    assert account.name == test_config['accountname']

def test_getAccount_cas_compte_inexistant(test_config):
    account = AccountService.getAccount("inexistant" + '@' + test_config['bss_domain'])
    assert account == None

def test_modifyAccount_cas_Normal(test_config):
    account_as_dict = { 'displayName': "Test2",
                        'telephoneNumber': "0223232323",
                        'carLicense': "test@DOMAIN",
                        'givenName': "prénom",
                        'sn': "nom accentué",
                        }
    account = AccountService.getAccount(test_config['accountname'])
    for attribute in account_as_dict:
        setattr(account, "_" + attribute, account_as_dict[attribute])

    AccountService.modifyAccount(account)
    account = AccountService.getAccount(test_config['accountname'])
    errors = 0
    for attribute in account_as_dict:
        if getattr(account, "_" + attribute) != account_as_dict[attribute]:
            errors = errors + 1
    assert errors == 0

def test_modifyAccount_cas_addZimlet(test_config):
    account = AccountService.getAccount(test_config['accountname'])
    account.addZimbraZimletAvailableZimlets("com_zimbra_emaildownloader")
    AccountService.modifyAccount(account)
    account = AccountService.getAccount(test_config['accountname'])
    assert "com_zimbra_emaildownloader" in account.zimbraZimletAvailableZimlets

def test_modifyAccount_cas_resetZimlet(test_config):
    account = AccountService.getAccount(test_config['accountname'])
    account.resetZimbraZimletAvailableZimlets()
    AccountService.modifyAccount(account)
    account = AccountService.getAccount(test_config['accountname'])
    assert "com_zimbra_emaildownloader" not in account.zimbraZimletAvailableZimlets

def test_modifyAliases_cas_departVideAjout1Alias(test_config):
    AccountService.modifyAccountAliases(test_config['accountname'], [test_config['accountalias']])
    account = AccountService.getAccount(test_config['accountname'])
    assert account.zimbraMailAlias == test_config['accountalias']

def test_modifyAliases_cas_depart1AliasPassageA2Alias(test_config):
    AccountService.modifyAccountAliases(test_config['accountname'], [test_config['accountalias'], test_config['autre_accountalias']])
    account = AccountService.getAccount(test_config['accountname'])
    assert (test_config['accountalias'] in account.zimbraMailAlias) and (test_config['autre_accountalias'] in account.zimbraMailAlias)

def test_modifyAliases_cas_depart2AliasPassageA1Alias(test_config):
    AccountService.modifyAccountAliases(test_config['accountname'], [test_config['autre_accountalias']])
    account = AccountService.getAccount(test_config['accountname'])
    assert account.zimbraMailAlias == test_config['autre_accountalias']

def test_deleteAccount_cas_Normal(test_config):
    AccountService.deleteAccount(test_config['accountname'])
    account = AccountService.getAccount(test_config['accountname'])
    assert account == None

def test_deleteAccount_cas_compteInexistant(test_config):
    with pytest.raises(ServiceException):
        AccountService.deleteAccount(test_config['accountname'])

