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
bss.setDomainKey({'x.fr', 'yourKey'})

# Recherche parmis les comptes
all_accounts = AccountService.getAllAccounts(domain='x.fr', limit=200, ldapQuery='mail=u*', attrs="carLicense,zimbraAccountStatus,zimbraHideInGAL")

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
./cli-bss.py --domain=x.fr --domainKey=yourKey --resetZimbraZimletAvailableZimlets --email=account_x@x.fr
cat liste_emails.txt | ./cli-bss.py --domain=x.fr --domainKey=yourKey --resetZimbraZimletAvailableZimlets
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
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyGroup --email=group@x.fr --jsonData=group.json -f displayName 'test'
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
./cli-bss.py --domain=x.fr --domainKey=yourKey --addRootShare --email=user1@x.fr --recipients=user2@x.fr --rights=sendAs
./cli-bss.py --domain=x.fr --domainKey=yourKey --removeRootShare --email=user1@x.fr --recipients=user2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey  -getAllResources
./cli-bss.py --domain=x.fr --domainKey=yourKey  -getAllResources --ldapQuery='(zimbraCalResType=Location)'
./cli-bss.py --domain=x.fr --domainKey=yourKey  --getResource --email=test_resource08012021@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey  --deleteResource --email=test_resource08012021@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey  --createResource --email=test_resource08012021@x.fr --userPassword=xxxxxxxx --zimbraCalResType=Location --displayName='Ressource de test'
./cli-bss.py --domain=x.fr --domainKey=yourKey  --modifyResource --email=test_resource08012021@x.fr --field displayName 'New displayName'
./cli-bss.py --domain=x.fr --domainKey=yourKey --getDefinition
./cli-bss.py --domain=x.fr --domainKey=yourKey --getHistoryDefinition
./cli-bss.py --domain=x.fr --domainKey=yourKey --deleteDefinition
./cli-bss.py --domain=x.fr --domainKey=yourKey --createDefinition --jsonData=/tmp/mailinglists.json
```

## Opérations implémentées

```
  --getAccount          rechercher un compte
  --createAccount       créer un compte
  --createAccountExt    créer un compte en spécifiant les paramètres via -f ou
                        --jsonData
  --modifyAccount       mettre à jour un compte
  --modifyAccountList   mettre à jour plusieurs compte
  --renameAccount       renommer un compte
  --deleteAccount       supprimer un compte
  --preDeleteAccount    pré-supprimer un compte (le compte est fermé et
                        renommé)
  --restorePreDeleteAccount
                        rétablir un compte pré-supprimé (compte fermé et
                        renommé)
  --getAllAccounts      rechercher tous les comptes du domaine
  --modifyPassword      modifier l'empreinte du mot de passe d'un compte
  --lockAccount         vérouiller un compte
  --activateAccount     (ré)activer un compte
  --closeAccount        fermer un compte
  --addAccountAlias     ajoute des aliases à un compte
  --removeAccountAlias  retire des aliases d'un compte
  --modifyAccountAliases
                        positionne une liste d'aliases pour un compte
                        (supprime des aliases existants si non mentionnés)
  --resetZimbraZimletAvailableZimlets
                        réinitialise la liste des zimlets pour un compte
                        (utile pour hériter du paramètre de la classe de
                        services)
  --getCos              rechercher une classe de service
  --getAllCos           rechercher toutes les classes de service du domaine
  --getDomain           informations sur un domaine
  --getDefinition       associer un nouveau JSON de définition des listes de
                        diffusion à un domaine (zimlet
                        net_renater_listes_diffusion)
  --getHistoryDefinition
                        lister l'historique mise à jour des JSON de définition
                        des listes de diffusion pour un domaine (zimlet
                        net_renater_listes_diffusion)
  --createDefinition    lister l'historique mise à jour des JSON de définition
                        des listes de diffusion pour un domaine (zimlet
                        net_renater_listes_diffusion)
  --deleteDefinition    supprimer le JSON de définition des listes de
                        diffusion pour un domaine (zimlet
                        net_renater_listes_diffusion)
  --countObjects        compter les objets d'un domaine
  --getResource         rechercher une resource
  --getAllResources     rechercher toutes les resources
  --deleteResource      Supprimer une resource
  --modifyResource      Modifier une resource
  --createResource      Créer une resource
  --getAllGroups        Afficher la liste des groupes et listes de
                        distribution
  --getGroup            Rechercher un groupe / une liste de distribution
  --getSendAsGroup      Lister les l’ensemble des comptes pouvant utiliser
                        l’adresse mail du groupe en adresse d’expédition.
  --createGroup         Créer un groupe / une liste de distribution.
  --createGroupExt      Créer un groupe / une liste de distribution en
                        spécifiant les paramètres via -f ou --jsonData
  --modifyGroup         Mettre à jour un groupe / une liste de distribution en
                        spécifiant les paramètres via -f et/ou --jsonData
  --deleteGroup         Supprimer un groupe / une liste de distribution.
  --addGroupAlias       Ajoute des alias à un groupe / une liste de
                        distribution.
  --removeGroupAlias    Supprime des alias à un groupe / une liste de
                        distribution.
  --setGroupAliases     Modifie les alias à un groupe / une liste de
                        distribution.
  --addGroupMember      Ajoute des membres à un groupe / une liste de
                        distribution.
  --removeGroupMember   Supprime des membres d'un groupe / d'une liste de
                        distribution.
  --setGroupMembers     Modifie les membres d'un groupe / d'une liste de
                        distribution.
  --addGroupSender      Ajoute des autorisations d'utilisation de l'adresse du
                        groupe ou de la liste de distribution par des comptes.
  --removeGroupSender   Supprime des autorisations d'utilisation de l'adresse
                        du groupe ou de la liste de distribution par des
                        comptes.
  --setGroupSenders     Modifie les autorisations d'utilisation de l'adresse
                        du groupe ou de la liste de distribution par des
                        comptes.
  --addRootShare        Ajouter un partage root d'une boites de service à un
                        ou plusieurs utilisateurs
  --removeRootShare     Retirer un partage root d'une boites de service à un
                        ou plusieurs utilisateurs
```

## Options
```
  -h, --help            show this help message and exit
  --bssUrl https://api.partage.renater.fr/service/domain
                        pour spécifier l'URL d'accès au BSS
  --domain mondomaine.fr
                        domaine cible sur le serveur Partage
  --domainKey 6b7ead4bd425836e8c
                        clé du domaine cible
  --email jchirac@mondomaine.fr
                        adresse mail passée en argument
  --recipients sendAs   droits à attribuer
  --rights autreuser@mondomaine.fr
                        adresse mail passée en argument
  --newEmail pdupont@mondomaine.fr
                        nouvelle adresse mail du compte
  --alias fcotton@mondomaine.fr
                        alias pour un compte
  --cosId 829a2781-c41e-4r4e2-b1a8-69f99dd20
                        identifiant de la classe de service
  --cosName staff_l_univ_rennes1
                        nom de la classe de service
  --limit 150           nombre d'entrées max pour une requête
  --offset 0            index de la première entrée à récupérer
  --ldapQuery mail=jean*
                        filtre LDAP pour une requête
  --attrs attrs=carLicense,zimbraAccountStatus,zimbraHideInGAL
                        sélection des attributs à retourner
  --sortBy mail         tri des résultats par attribut
  --userPassword {ssha}HpqRjlh1WEha+6or95YkqA
                        empreinte du mot de passe utilisateur
  --asJson              option pour exporter un compte au format JSON
  --jsonData /tmp/myAccount.json
                        fichier contenant des données JSON
  --fullData            Récupérer toutes les informations dans les requêtes
                        sur les groupes. Attention, c'est lent.
  --field name value, -f name value
                        nom et valeur d'un champ du compte
  --member example@example.org
                        Membre(s) d'un groupe ou d'une liste de distribution.
  --sender example@example.org
                        Compte autorisé à utiliser l'adresse mail d'un groupe
                        ou d'une liste de distribution en adresse
                        d'expédition.
  --zimbraCalResType Location
                        Type de la resource
  --displayName Resource
                        Nom de la resource
  --type userAccount    type d'objet à rechercher (userAccount, alias, dl ou
                        calresource)
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
