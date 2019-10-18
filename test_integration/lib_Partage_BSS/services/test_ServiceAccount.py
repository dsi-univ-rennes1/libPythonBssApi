import pytest
from lib_Partage_BSS.models.Account import Account
from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS.services import AccountService, BSSConnexion
import time as timer

def create_account(name):
    account = AccountService.getAccount(name)
    if account == None:
        AccountService.createAccount(name,"{ssha}BIDON")

def delete_account(name):
    account = AccountService.getAccount(name)
    if account != None:
        AccountService.deleteAccount(name)

def create_connexion(config):
    timer.sleep(1)
    con = BSSConnexion()
    if 'bss_url' in config:
        con.url = config['bss_url']
    con.setDomainKey({config['bss_domain']: config['bss_domain_key']})
    return BSSConnexion()

def test_init_variables(test_config):
    global accountname, autre_accountname, accountalias, autre_accountalias, con
    con = create_connexion(test_config)
    accountname = "test_creation_lib_python" + '@' + test_config['bss_domain']
    accountalias = "alias_" + accountname
    autre_accountalias = "alias_" + accountname
    autre_accountname = "autre_account_test_creation_lib_python" + '@' + test_config['bss_domain']

def test_cleanup_bss_environment(test_config):
    print("Cleanup BSS environment before running tests...")
    delete_account(accountname)
    delete_account(autre_accountname)

def test_createAccount_cas_normal(test_config):
    AccountService.createAccount(accountname, "{ssha}BIDON")
    account = AccountService.getAccount(accountname)
    assert account.name == accountname

def test_createAccount_cas_compteExistant(test_config):
    with pytest.raises(ServiceException):
        AccountService.createAccount(accountname, "{ssha}BIDON")

def test_getAccount_cas_normal(test_config):
    account = AccountService.getAccount(accountname)
    assert account.name == accountname

def test_getAccount_cas_compte_inexistant(test_config):
    account = AccountService.getAccount("inexistant" + '@' + test_config['bss_domain'])
    assert account == None

def test_modifyAccount_cas_Normal(test_config):
    account = AccountService.getAccount(accountname)
    account.displayName = "Test2"
    AccountService.modifyAccount(account)
    account = AccountService.getAccount(accountname)
    assert account.displayName == "Test2"

def test_set_telephone_number(test_config):
    account = AccountService.getAccount(accountname)
    account.telephoneNumber = "0223232323"
    AccountService.modifyAccount(account)
    account = AccountService.getAccount(accountname)
    assert account.telephoneNumber == "0223232323"

def test_set_car_license(test_config):
    account = AccountService.getAccount(accountname)
    account.carLicense = "test@DOMAIN"
    AccountService.modifyAccount(account)
    account = AccountService.getAccount(accountname)
    assert account.carLicense == "test@DOMAIN"

def test_set_given_name(test_config):
    account = AccountService.getAccount(accountname)
    account.givenName = "prénom"
    AccountService.modifyAccount(account)
    account = AccountService.getAccount(accountname)
    assert account.givenName == "prénom"

def test_set_surname(test_config):
    account = AccountService.getAccount(accountname)
    account.sn = "nom accentué"
    AccountService.modifyAccount(account)
    account = AccountService.getAccount(accountname)
    assert account.sn == "nom accentué"

def test_modifyAliases_cas_departVideAjout1Alias(test_config):
    AccountService.modifyAccountAliases(accountname, [accountalias])
    account = AccountService.getAccount(accountname)
    assert account.zimbraMailAlias == accountalias

def test_modifyAliases_cas_depart1AliasPassageA2Alias(test_config):
    AccountService.modifyAccountAliases(accountname, [accountalias, autre_accountalias])
    account = AccountService.getAccount(accountname)
    assert (accountalias in account.zimbraMailAlias) and (autre_accountalias in account.zimbraMailAlias)

def test_modifyAliases_cas_depart2AliasPassageA1Alias(test_config):
    AccountService.modifyAccountAliases(accountname, [autre_accountalias])
    account = AccountService.getAccount(accountname)
    assert account.zimbraMailAlias == autre_accountalias

def test_deleteAccount_cas_Normal(test_config):
    AccountService.deleteAccount(accountname)
    account = AccountService.getAccount(accountname)
    assert account == None

def test_deleteAccount_cas_compteInexistant(test_config):
    with pytest.raises(ServiceException):
        AccountService.deleteAccount(accountname)

