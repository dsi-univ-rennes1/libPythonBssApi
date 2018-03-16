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

## Documentation

## Exemple

```
from lib_Partage_BSS.models.Account import Account
from lib_Partage_BSS.services import AccountService
from lib_Partage_BSS.services.BSSConnexionService import BSSConnexion

# Connexion au BSS
bss = BSSConnexion()
bss.setDomainKey('x.fr', 'yourKey')

# Recherche parmis les comptes
all_accounts = AccountService.getAllAccounts(domain='x.fr', limit=200, 'mail=u*')

# Consultation d'un compte
account = AccountService.getAccount('user@x.fr')

# Création d'un compte
AccountService.createAccount(name='user@x.fr', userPassword='{SSHA}yourHash', cosId='yourCos')
```

## Client en ligne de commande
Le script `cli-bss.py` est un client BSS en ligne de commande.

Les arguments `--domain` et `--domainKey` doivent être fournis pour chaque appel.

Exemples d'appel :
```
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=u*'
./cli-bss.py --domain=x.fr --domainKey=yourKey --createAccount --email=user@x.fr --cosId=yourCos --userPassword={SSHA}yourHash
./cli-bss.py --domain=x.fr --domainKey=yourKey --deleteAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyPassword --email=user@x.fr  --userPassword={SSHA}yourHash
./cli-bss.py --domain=x.fr --domainKey=yourKey --lockAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=us*'
./cli-bss.py --domain=x.fr --domainKey=yourKey --closeAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --preDeleteAccount --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --restorePreDeleteAccount --email=readytodelete_2018-03-14-13-37-15_user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccount --jsonData=account.json --email=user@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --renameAccount --email=user@x.fr --newEmail=user2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --addAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --removeAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr
./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccountAliases --email=user@x.fr --alias=alias3@x.fr --alias=alias4@x.fr
```

## License

La bibilothèque `lib_Partage_BSS` est distribuée sous [la license Apache 2.0](https://www.apache.org/licenses/)
