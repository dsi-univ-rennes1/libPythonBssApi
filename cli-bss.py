#!/usr/bin/python
# This Python file uses the following encoding: utf-8# Script pour faire mes 1er pas en Python
# O.Salaün (Univ Rennes1) : client en ligne de commande pour lib_Partage_BSS

# Exemples d'appel :
#  cli-bss.py --domain=ur1.fr --getAccount=odile.germes@ur1.fr
#  cli-bss.py --domain=ur1.fr --getAllAccounts


import argparse, sys
import pprint
import json

from lib_Partage_BSS.exceptions import ServiceException, NameException
from lib_Partage_BSS.models.Account import Account
from lib_Partage_BSS.services import AccountService
from lib_Partage_BSS.services.BSSConnexionService import BSSConnexion

printer = pprint.PrettyPrinter(indent=4)

epilog = "Exemples d'appel :\n" + \
    "./cli-bss.py --domain=x.fr --preAuthKey=yourKey --getAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=u*'\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --createAccount --email=user@x.fr --cosId=yourCos --userPassword={SSHA}yourHash\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --deleteAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --modifyPassword --email=user@x.fr  --userPassword={SSHA}yourHash\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --lockAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=us*'\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --closeAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --preDeleteAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --restorePreDeleteAccount --email=readytodelete_2018-03-14-13-37-15_user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --modifyAccount --jsonData=account.json --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --renameAccount --email=user@x.fr --newEmail=user2@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --addAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --removeAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --preAuthKey=yourKey --modifyAccountAliases --email=user@x.fr --alias=alias3@x.fr --alias=alias4@x.fr\n"

parser = argparse.ArgumentParser(description="Client en ligne de commande pour l'API BSS Partage", epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--domain', required=True, metavar='mondomaine.fr', help="domaine cible sur le serveur Partage")
parser.add_argument('--preAuthKey', required=True, metavar="6b7ead4bd425836e8c", help="clé de preAuth pour le domaine cible")
parser.add_argument('--email', metavar='jchirac@mondomaine.fr', help="adresse mail passée en argument")
parser.add_argument('--newEmail', metavar='pdupont@mondomaine.fr', help="nouvelle adresse mail du compte")
parser.add_argument('--alias', action='append', metavar='fcotton@mondomaine.fr', help="alias pour un compte")
parser.add_argument('--cosId', metavar='829a2781-c41e-4r4e2-b1a8-69f99dd20', help="identifiant de la classe de service")
parser.add_argument('--limit', metavar='150', type=int, default=100, help="nombre d'entrées max pour une requête")
parser.add_argument('--ldapQuery', metavar='mail=jean*', help="filtre LDAP pour une requête")
parser.add_argument('--userPassword', metavar='{ssha}HpqRjlh1WEha+6or95YkqA', help="empreinte du mot de passe utilisateur")
parser.add_argument('--asJson', action='store_const', const=True, help="option pour exporter un compte au format JSON")
parser.add_argument('--jsonData', metavar='/tmp/myAccount.json', type=argparse.FileType('r'), help="fichier contenant des données JSON")

group = parser.add_argument_group('Opérations implémentées :')
group.add_argument('--getAccount', action='store_const', const=True, help="rechercher un compte")
group.add_argument('--createAccount', action='store_const', const=True, help="créer un compte")
group.add_argument('--modifyAccount', action='store_const', const=True, help="mettre à jour un compte")
group.add_argument('--renameAccount', action='store_const', const=True, help="renommer un compte")
group.add_argument('--deleteAccount', action='store_const', const=True, help="supprimer un compte")
group.add_argument('--preDeleteAccount', action='store_const', const=True, help="pré-supprimer un compte (le compte est fermé et renommé)")
group.add_argument('--restorePreDeleteAccount', action='store_const', const=True, help="rétablir un compte pré-supprimé (compte fermé et renommé)")
group.add_argument('--getAllAccounts', action='store_const', const=True, help="rechercher tous les comptes du domaine")
group.add_argument('--modifyPassword', action='store_const', const=True, help="modifier l'empreinte du mot de passe d'un compte")
group.add_argument('--lockAccount', action='store_const', const=True, help="vérouiller un compte")
group.add_argument('--activateAccount', action='store_const', const=True, help="(ré)activer un compte")
group.add_argument('--closeAccount', action='store_const', const=True, help="fermer un compte")
group.add_argument('--addAccountAlias', action='store_const', const=True, help="ajoute des aliases à un compte")
group.add_argument('--removeAccountAlias', action='store_const', const=True, help="retire des aliases d'un compte")
group.add_argument('--modifyAccountAliases', action='store_const', const=True, help="positionne une liste d'aliases pour un compte (supprime des aliases existants si non mentionnés)")

args = vars(parser.parse_args())

# Connexion au BSS
try:
    bss = BSSConnexion()
    bss.setDomainKey(domain=args['domain'], key=args['preAuthKey'])

except Exception as err:
    print("Echec de connexion : %s" % err)
    sys.exit(2)

if args['getAllAccounts'] == True:

    try:
        if args['ldapQuery']:
            all_accounts = AccountService.getAllAccounts(domain=args['domain'], limit=args['limit'], ldapQuery=args['ldapQuery'])
        else:
            all_accounts = AccountService.getAllAccounts(domain=args['domain'], limit=args['limit'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("%d comptes retournés :" % len(all_accounts))
    for account in all_accounts:
        print("Compte %s :" % account.getName)
        print(account.showAttr())

elif args['getAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        account = AccountService.getAccount(args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    if args['asJson']:
        print(json.dumps(account.__dict__, sort_keys=True, indent=4))

    else:
        print("Informations sur le compte %s :" % account.getName)
        print(account.showAttr())

elif args['deleteAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        AccountService.deleteAccount(args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été supprimé" % args['email'])



elif args['preDeleteAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        AccountService.preDeleteAccount(args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été préparé pour une suppression ultérieure" % args['email'])


elif args['restorePreDeleteAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        AccountService.restorePreDeleteAccount(args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été rétabli" % args['email'])

elif args['createAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['userPassword']:
        raise Exception("Missing 'userPassword' argument")

    if not args['cosId']:
        raise Exception("Missing 'cosId' argument")

    try:
        AccountService.createAccount(name=args['email'], userPassword=args['userPassword'], cosId=args['cosId'] )

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été créé" % args['email'])

elif args['modifyAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['jsonData']:
        raise Exception("Missing 'jsonData' argument")

    try:
        account_as_json = json.load(args['jsonData'])

    except Exception as err:
        print("Echec chargement fichier JSON %s : %s" % (args['jsonData'], err))
        sys.exit(2)

    try:
        account = Account(name=args['email'])

        # On exécute le setter pour chaque attribut présent dans le fichier jsonData
        for key, value in account_as_json.items():
            getattr(account, 'set'+key.capitalize())(value)

        AccountService.modifyAccount(account=account)

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été mis à jour" % args['email'])

elif args['renameAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['newEmail']:
        raise Exception("Missing 'newEmail' argument")

    try:
        AccountService.renameAccount(name=args['email'], newName=args['newEmail'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été renommé %s" % (args['email'], args['newEmail']))

elif args['modifyPassword'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['userPassword']:
        raise Exception("Missing 'userPassword' argument")

    try:
        AccountService.modifyPassword(name=args['email'], newUserPassword=args['userPassword'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le mot de passe du compte %s a été mis à jour" % args['email'])

elif args['lockAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        AccountService.lockAccount(name=args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été vérouillé" % args['email'])


elif args['activateAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        AccountService.activateAccount(name=args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été (ré)activé" % args['email'])

elif args['closeAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        AccountService.closeAccount(name=args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été fermé" % args['email'])

elif args['addAccountAlias'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['alias']:
        raise Exception("Missing 'alias' argument")

    try:
        for alias in args['alias']:
            AccountService.addAccountAlias(name=args['email'], newAlias=alias)

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Les aliases %s ont été ajoutés au compte %s" % (args['alias'], args['email']))

elif args['removeAccountAlias'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['alias']:
        raise Exception("Missing 'alias' argument")

    try:
        for alias in args['alias']:
            AccountService.removeAccountAlias(name=args['email'], aliasToDelete=alias)

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Les aliases %s ont été retirés du compte %s" % (args['alias'], args['email']))

elif args['modifyAccountAliases'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['alias']:
        raise Exception("Missing 'alias' argument")

    try:
        AccountService.modifyAccountAliases(name=args['email'], listOfAliases=args['alias'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Les aliases pour le compte %s ont été positionnés à %s" % (args['email'], args['alias']))

else:
    print("Aucune opération à exécuter")
