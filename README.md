# Bibliothèque Python pour l'API BSS du service Partage

La plateforme Partage est proposé par RENATER aux organismes 
d'enseignement supérieur et de recherche français. L'API BSS, 
développée par RENATER, est une API REST donne accès à certaines 
fonctions de l'API de provisioning de Zimbra.
* [SOAP API Reference](https://wiki.zimbra.com/wiki/SOAP_API_Reference_Material_Beginning_with_ZCS_8), Zimbra
* [API BSS Documentation](https://dashboard.partage.renater.fr/api_bss_documentation.html), RENATER

L'accès à l'API BSS est réservée aux administrateurs de chaque organisme raccordé à 
Partage et nécessite une authentification via une clé de pré-authentification.

## Motivation pour le développement de cette bibliothèque

Début 2018, l'Université de Rennes 1 souscrit au service Partage et développe la 
bibliothèque `lib_Partage_BSS` pour mettre en oeuvre le provisioning des comptes utilisateurs sur Partage. 

## Installation et prérequis

```
git clone https://github.com/dsi-univ-rennes1/libPythonBssApi.git
cd libPythonBssApi
python3.5 -m venv venv
venv/bin/pip install --requirement requirements.txt
./cli-bss.py --help
```

### Méthode alternative: pipenv
```
pip3 install pipenv
git clone https://github.com/dsi-univ-rennes1/libPythonBssApi.git
cd libPythonBssApi
pipenv install --dev
pipenv run python ./cli-bss.py --help
```

## Documentation

## Exemples

### Se connecter au BSS, rechercher de comptes par filtre et créer un compte

```
from lib_Partage_BSS.models.Account import Account
from lib_Partage_BSS.services import AccountService
from lib_Partage_BSS.services.BSSConnexionService import BSSConnexion

# Connexion au BSS
bss = BSSConnexion()
bss.setDomainKey('x.fr', 'yourKey')

# Recherche parmis les comptes
all_accounts = AccountService.getAllAccounts(domain='x.fr', limit=200, 'mail=u*', , attrs="carLicense,zimbraAccountStatus,zimbraHideInGAL")

# Consultation d'un compte
account = AccountService.getAccount('user@x.fr')

# Création d'un compte
AccountService.createAccount(name='user@x.fr', userPassword='{SSHA}yourHash', cosId='yourCos')
```

### getAllAccounts en exploitant la pagination
``````
from lib_Partage_BSS.services import AccountService
from lib_Partage_BSS.services.BSSConnexionService import BSSConnexion

listDomainKey = {"x.fr": "yourKey"}

bss = BSSConnexion()
bss.setDomainKey(listDomainKey=listDomainKey)

offset = 0
limit = 100
while True:

    print("getAllAccounts(%i)..." % offset)
    list_accounts_partage = AccountService.getAllAccounts(domain="x.fr", limit=limit, offset=offset, ldapQuery="(!(zimbraHideInGAL=TRUE))")

    if len(list_accounts_partage) == 0:
        break

    for account_from_all in list_accounts_partage:
        print("\t%s" % account_from_all.name)

    offset += limit
``````

## Client en ligne de commande
Le script `cli-bss.py` est un client BSS en ligne de commande.

Les arguments `--domain` et `--domainKey` doivent être fournis pour chaque appel.

Exemples d'appel :
```
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAccount --email=user@x.fr
./cli-bss.py --bssUrl=https://api.partage.renater.fr/service/domain --domain=x.fr --domainKey=yourKey --getAllAccounts
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=u*'
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --sortBy=mail
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=u*' --attrs='carLicense,zimbraAccountStatus,zimbraHideInGAL'
./cli-bss.py --domain=x.fr --domainKey=yourKey --createAccount --email=user@x.fr --cosId=yourCos --userPassword={SSHA}yourHash
./cli-bss.py --domain=x.fr --domainKey=yourKey --createAccountExt -f name user@x.fr -f zimbraHideInGal oui --userPassword={SSHA}someHash
./cli-bss.py --domain=x.fr --domainKey=yourKey --deleteAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyPassword --email=user@x.fr  --userPassword={SSHA}yourHash
./cli-bss.py --domain=x.fr --domainKey=yourKey --lockAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=us*'
./cli-bss.py --domain=x.fr --domainKey=yourKey --closeAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --preDeleteAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --restorePreDeleteAccount --email=readytodelete_2018-03-14-13-37-15_user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccount --jsonData=account.json --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccountList --field zimbraAccountStatus closed
./cli-bss.py --domain=x.fr --domainKey=yourKey --renameAccount --email=user@x.fr --newEmail=user2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --addAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --removeAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccountAliases --email=user@x.fr --alias=alias3@x.fr --alias=alias4@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --getCos --cosName=etu_s_xx
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllCos
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllGroups
./cli-bss.py --domain=x.fr --domainKey=yourKey --getDomain
./cli-bss.py --domain=x.fr --domainKey=yourKey --countObjects --type=userAccount
./cli-bss.py --domain=x.fr --domainKey=yourKey --getGroup --email=testgroup1@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --getGroup --email=testgroup1@x.fr --fullData
./cli-bss.py --domain=x.fr --domainKey=yourKey --getSendAsGroup --email=testgroup1@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --createGroup --email=testgroup2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --createGroupExt -f name testgroup4@x.fr -f displayName 'Groupe 4' -f zimbraMailStatus disabled
./cli-bss.py --domain=x.fr --domainKey=yourKey --createGroupExt --jsonData=/tmp/data.json
./cli-bss.py --domain=x.fr --domainKey=yourKey --deleteGroup --email=testgroup6@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --addGroupAlias --email=testgroup4@x.fr --alias=alias@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --removeGroupAlias --email=testgroup4@x.fr --alias=alias@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --setGroupAlias --email=testgroup4@x.fr --alias=alias2@x.fr --alias=alias3@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --addGroupMember --email=testgroup1@x.fr --member=member01@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --removeGroupMember --email=testgroup1@x.fr --member=member01@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --setGroupMember --email=testgroup1@x.fr --member=member01@x.fr --member=member02@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --addGroupSender --email=testgroup1@x.fr --sender=sender03@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --removeGroupSender --email=testgroup1@x.fr --sender=sender03@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --setGroupSender --email=testgroup1@x.fr --sender=sender03@x.fr  --sender=sender05@x.fr
```

## Tests

Vous pouvez exécuter les tests unitaires et les tests d'intégration via l'utilitaire `pytest`.

Lancer les tests unitaires :
```
venv/bin/pytest -v test_unitaire/
================================================== test session starts ===================================================
platform linux -- Python 3.5.2, pytest-3.6.3, py-1.5.4, pluggy-0.6.0 -- /home/salaun/PycharmProjects/libPythonBssApi/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/salaun/PycharmProjects/libPythonBssApi, inifile:
plugins: mock-1.10.0
collected 50 items                                                                                                       

test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casNormal PASSED                        [  2%]
test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casNormalSurAutreDomain PASSED          [  4%]
test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casPreAuthEchec PASSED                  [  6%]
test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casDomainNonString PASSED               [  8%]
test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casDomainNonValide PASSED               [ 10%]
test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casDomainNonPresentDansConfig PASSED    [ 12%]
test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_4minApresCreation PASSED                [ 14%]
test_unitaire/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_5minApresCreation PASSED                [ 16%]
test_unitaire/lib_Partage_BSS/services/test_ServiceAccount.py::test_init_cas_nom_vallide PASSED                    [ 18%]
test_unitaire/lib_Partage_BSS/services/test_ServiceAccount.py::test_init_cas_nom_non_vallide PASSED                [ 20%]
test_unitaire/lib_Partage_BSS/services/test_ServiceAccount.py::test_getAccount_cas_compte_existant PASSED          [ 22%]
test_unitaire/lib_Partage_BSS/services/test_ServiceAccount.py::test_getAccount_cas_compte_inexistant PASSED        [ 24%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casTrueSansSeparateur PASSED             [ 26%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casTrueAvecTiret PASSED                  [ 28%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casTrueAvecPoint PASSED                  [ 30%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casTrueAvecEspace PASSED                 [ 32%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casTrueAvecUnderscore PASSED             [ 34%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casTrueAvecSlash PASSED                  [ 36%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casTrueVide PASSED                       [ 38%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casFalseAvecLettre PASSED                [ 40%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsNum_casFalseAvecCaractereSpecial PASSED      [ 42%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casTrueAvecDebutEn1Partie PASSED [ 44%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casTrueAvecDebutEn2Parties PASSED [ 46%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casTrueVide PASSED               [ 48%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casFalseSansDomain PASSED        [ 50%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casFalseSansExtensionDeDomain PASSED [ 52%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casFalseSansAdresseMaisAvecDomaine PASSED [ 54%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casFalseDomainTropCourt PASSED   [ 56%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsMailAddress_casFalseDomainTropLong PASSED    [ 58%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsDomain_casTrueDomainAvecExtension2caracteres PASSED [ 60%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsDomain_casTrueDomainAvecExtension4caracteres PASSED [ 62%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsDomain_casTrueDomainAvecSousDomaine PASSED   [ 64%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsDomain_casFalseDomainAvecExtension5caracteres PASSED [ 66%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsDomain_casFalseDomainAvecExtension1caractere PASSED [ 68%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsPreDeleteAccount_casTrue PASSED              [ 70%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsPreDeleteAccount_casFalsePasreadytodeleteAuDebut PASSED [ 72%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsPreDeleteAccount_casFalseMauvaisFormatDate PASSED [ 74%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsPreDeleteAccount_casFalseDateIncomplete PASSED [ 76%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkIsPreDeleteAccount_casFalsePasAdresseMailALaFin PASSED [ 78%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkResponseStatus_casTrue0 PASSED                 [ 80%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_checkResponseStatus_casFalse1 PASSED                [ 82%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeBooleanToString_casTrueParamTrue PASSED       [ 84%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeBooleanToString_casTrueParamFalse PASSED      [ 86%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeStringToBoolean_casTrueParamTRUE PASSED       [ 88%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeStringToBoolean_casTrueParamFALSE PASSED      [ 90%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeStringToBoolean_casNoneParamAUTRE PASSED      [ 92%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeToInt_casTrueInteger PASSED                   [ 94%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeToInt_casException PASSED                     [ 96%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeTimestampToDate_casOk PASSED                  [ 98%]
test_unitaire/lib_Partage_BSS/utils/test_CheckMethods.py::test_changeDateToTimestamp_casOk PASSED                  [100%]

=============================================== 50 passed in 18.23 seconds ===============================================
```


L'exécution des tests d'intégration nécessite que vous ayez accès à un environnement BSS fourni par RENATER. Lancer les tests d'intégration :
```
$ venv/bin/pytest -v --bss_domain=x.fr --bss_domain_key=yourKey test_integration/lib_Partage_BSS/services/
================================================== test session starts ===================================================
platform linux -- Python 3.5.2, pytest-3.6.3, py-1.5.4, pluggy-0.6.0 -- /home/salaun/PycharmProjects/libPythonBssApi/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/salaun/PycharmProjects/libPythonBssApi, inifile:
plugins: mock-1.10.0
collected 40 items                                                                                                       

test_integration/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casNormal PASSED                     [  2%]
test_integration/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casDomainFaux PASSED                 [  5%]
test_integration/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_casDomainNonPresent PASSED           [  7%]
test_integration/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_8sApresCreation PASSED               [ 10%]
test_integration/lib_Partage_BSS/services/test_BSSConnexion.py::test_getToken_5minApresCreation PASSED             [ 12%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_init_variables PASSED                       [ 15%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_cleanup_bss_environment PASSED              [ 17%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_createAccount_cas_normal PASSED             [ 20%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_createAccount_cas_compteExistant PASSED     [ 22%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_getAccount_cas_normal PASSED                [ 25%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_getAccount_cas_compte_inexistant PASSED     [ 27%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_modifyAccount_cas_Normal PASSED             [ 30%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_modifyAliases_cas_departVideAjout1Alias PASSED [ 32%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_modifyAliases_cas_depart1AliasPassageA2Alias PASSED [ 35%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_modifyAliases_cas_depart2AliasPassageA1Alias PASSED [ 37%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_deleteAccount_cas_Normal PASSED             [ 40%]
test_integration/lib_Partage_BSS/services/test_ServiceAccount.py::test_deleteAccount_cas_compteInexistant PASSED   [ 42%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_init_variables PASSED                         [ 45%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_cleanup_bss_environment PASSED                [ 47%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_createGroup_cas_normal PASSED                 [ 50%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_createGroup_cas_groupeExistant PASSED         [ 52%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_getGroup_cas_normal PASSED                    [ 55%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_getGroup_cas_groupe_inexistant PASSED         [ 57%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_addGroupAliases_cas_Normal PASSED             [ 60%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_addGroupAliases_cas_groupe_existant PASSED    [ 62%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_updateGroupAliases_cas_Normal PASSED          [ 65%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_removeGroupAliases_cas_Normal PASSED          [ 67%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_updateGroupAliases_cas_domaine_incorrect PASSED [ 70%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_removeGroupAliases_cas_alias_inconnu PASSED   [ 72%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_addGroupMember_cas_Normal PASSED              [ 75%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_updateGroupMembers_cas_Normal PASSED          [ 77%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_removeGroupMembers_cas_Normal PASSED          [ 80%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_removeGroupMembers_cas_alias_inconnu PASSED   [ 82%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_addGroupSenders_cas_Normal PASSED             [ 85%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_addGroupSenders_cas_compte_inconnu PASSED     [ 87%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_updateGroupSenders_cas_Normal PASSED          [ 90%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_removeGroupSenders_cas_Normal PASSED          [ 92%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_removeGroupSenders_cas_alias_inconnu PASSED   [ 95%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_deleteGroup_cas_normal PASSED                 [ 97%]
test_integration/lib_Partage_BSS/services/test_ServiceGroup.py::test_deleteGroup_cas_groupe_inexistant PASSED      [100%]

============================================== 40 passed in 377.01 seconds ===============================================
```

Vous pouvez exécuter les tests d'intégration sur l'environnement de préprod de Renater en spécifiant l'argument `--bss_url` à `pytest`.

## License

La bibliothèque `lib_Partage_BSS` est distribuée sous [la license Apache 2.0](https://www.apache.org/licenses/)
