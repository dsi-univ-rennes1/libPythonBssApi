#!venv/bin/python
# This Python file uses the following encoding: utf-8# Script pour faire mes 1er pas en Python
# O.Salaün (Univ Rennes1) : client en ligne de commande pour lib_Partage_BSS

import argparse, sys, re
import pprint
import json

from lib_Partage_BSS.exceptions import *
from lib_Partage_BSS.models.Account import Account, importJsonAccount
from lib_Partage_BSS.models.Group import Group
from lib_Partage_BSS.services import AccountService , GroupService, ResourceService
from lib_Partage_BSS.models.COS import COS
from lib_Partage_BSS.services import COSService
from lib_Partage_BSS.services import DomainService
from lib_Partage_BSS.services.BSSConnexionService import BSSConnexion
from lib_Partage_BSS.services import PartageService

printer = pprint.PrettyPrinter(indent=4)

epilog = "Exemples d'appel :\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getAccount --email=user@x.fr\n" + \
    "./cli-bss.py --bssUrl=https://api.partage.renater.fr/service/domain --domain=x.fr --domainKey=yourKey --getAllAccounts\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=u*'\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --sortBy=mail\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=u*' --attrs='carLicense,zimbraAccountStatus,zimbraHideInGAL'\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --createAccount --email=user@x.fr --cosId=yourCos --userPassword={SSHA}yourHash\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --createAccountExt " + \
        "-f name user@x.fr -f zimbraHideInGal oui --userPassword={SSHA}someHash\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --deleteAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyPassword --email=user@x.fr  --userPassword={SSHA}yourHash\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --lockAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllAccounts --limit=200 --ldapQuery='mail=us*'\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --closeAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --preDeleteAccount --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --restorePreDeleteAccount --email=readytodelete_2018-03-14-13-37-15_user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --resetZimbraZimletAvailableZimlets --email=account_x@x.fr\n" + \
	"cat liste_emails.txt | ./cli-bss.py --domain=x.fr --domainKey=yourKey --resetZimbraZimletAvailableZimlets\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccount --jsonData=account.json --email=user@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccountList --field zimbraAccountStatus closed\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --renameAccount --email=user@x.fr --newEmail=user2@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --addAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --removeAccountAlias --email=user@x.fr --alias=alias1@x.fr --alias=alias2@x.fr\n" + \
	"./cli-bss.py --domain=x.fr --domainKey=yourKey --modifyAccountAliases --email=user@x.fr --alias=alias3@x.fr --alias=alias4@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getCos --cosName=etu_s_xx\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllCos\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getAllGroups\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getDomain\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --countObjects --type=userAccount\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getGroup --email=testgroup1@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getGroup --email=testgroup1@x.fr --fullData\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --getSendAsGroup --email=testgroup1@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --createGroup --email=testgroup2@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --createGroupExt -f name testgroup4@x.fr -f displayName 'Groupe 4' -f zimbraMailStatus disabled\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --createGroupExt --jsonData=/tmp/data.json\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --deleteGroup --email=testgroup6@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --addGroupAlias --email=testgroup4@x.fr --alias=alias@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --removeGroupAlias --email=testgroup4@x.fr --alias=alias@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --setGroupAlias --email=testgroup4@x.fr --alias=alias2@x.fr --alias=alias3@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --addGroupMember --email=testgroup1@x.fr --member=member01@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --removeGroupMember --email=testgroup1@x.fr --member=member01@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --setGroupMember --email=testgroup1@x.fr --member=member01@x.fr --member=member02@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --addGroupSender --email=testgroup1@x.fr --sender=sender03@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --removeGroupSender --email=testgroup1@x.fr --sender=sender03@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --setGroupSender --email=testgroup1@x.fr --sender=sender03@x.fr  --sender=sender05@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey --addRootShare --email=user1@x.fr --recipients=user2@x.fr --rights=sendAs\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey  -getAllResources\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey  --getResource --email=test_resource08012021@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey  --deleteResource --email=test_resource08012021@x.fr\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey  --createResource --email=test_resource08012021@x.fr --userPassword=xxxxxxxx --zimbraCalResType=Location --displayName='Ressource de test'\n" + \
    "./cli-bss.py --domain=x.fr --domainKey=yourKey  --modifyResource --email=test_resource08012021@x.fr --field displayName 'New displayName'\n"

parser = argparse.ArgumentParser(description="Client en ligne de commande pour l'API BSS Partage", epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--bssUrl', metavar='https://api.partage.renater.fr/service/domain', help="pour spécifier l'URL d'accès au BSS")
parser.add_argument('--domain', required=True, metavar='mondomaine.fr', help="domaine cible sur le serveur Partage")
parser.add_argument('--domainKey', required=True, metavar="6b7ead4bd425836e8c", help="clé du domaine cible")
parser.add_argument('--email', metavar='jchirac@mondomaine.fr', help="adresse mail passée en argument")
parser.add_argument('--recipients', metavar='sendAs', help="droits à attribuer")
parser.add_argument('--rights', metavar='autreuser@mondomaine.fr', help="adresse mail passée en argument")
parser.add_argument('--newEmail', metavar='pdupont@mondomaine.fr', help="nouvelle adresse mail du compte")
parser.add_argument('--alias', action='append', metavar='fcotton@mondomaine.fr', help="alias pour un compte")
parser.add_argument('--cosId', metavar='829a2781-c41e-4r4e2-b1a8-69f99dd20', help="identifiant de la classe de service")
parser.add_argument('--cosName', metavar='staff_l_univ_rennes1', help="nom de la classe de service")
parser.add_argument('--limit', metavar='150', type=int, default=100, help="nombre d'entrées max pour une requête")
parser.add_argument('--offset', metavar='0', type=int, default=0,
        help="index de la première entrée à récupérer")
parser.add_argument('--ldapQuery', metavar='mail=jean*', help="filtre LDAP pour une requête")
parser.add_argument('--attrs', metavar='attrs=carLicense,zimbraAccountStatus,zimbraHideInGAL', help="sélection des attributs à retourner")
parser.add_argument('--sortBy', metavar='mail', help="tri des résultats par attribut")
parser.add_argument('--userPassword', metavar='{ssha}HpqRjlh1WEha+6or95YkqA', help="empreinte du mot de passe utilisateur")
parser.add_argument('--asJson', action='store_const', const=True, help="option pour exporter un compte au format JSON")
parser.add_argument('--jsonData', metavar='/tmp/myAccount.json', type=argparse.FileType('r'), help="fichier contenant des données JSON")
parser.add_argument( '--fullData' ,
    action = 'store_true' ,
    help = '''Récupérer toutes les informations dans les requêtes sur les
              groupes. Attention, c'est lent.''' )
parser.add_argument('--field' , '-f' ,
    action='append' , nargs=2 ,
    metavar=('name','value') , help="nom et valeur d'un champ du compte")
parser.add_argument( '--member' , action = 'append' ,
    metavar = 'example@example.org' ,
    help = '''Membre(s) d'un groupe ou d'une liste de distribution.''' )
parser.add_argument( '--sender' , action = 'append' ,
    metavar = 'example@example.org' ,
    help = '''Compte autorisé à utiliser l'adresse mail d'un groupe ou d'une
              liste de distribution en adresse d'expédition.''' )
parser.add_argument('--zimbraCalResType', metavar='Location', help="Type de la resource")
parser.add_argument('--displayName', metavar='Resource', help="Nom de la resource")

group = parser.add_argument_group('Opérations implémentées :')
group.add_argument('--getAccount', action='store_const', const=True, help="rechercher un compte")
group.add_argument('--createAccount', action='store_const', const=True, help="créer un compte")
group.add_argument('--createAccountExt',
    action='store_const', const=True,
    help="créer un compte en spécifiant les paramètres via -f ou --jsonData")
group.add_argument('--modifyAccount', action='store_const', const=True, help="mettre à jour un compte")
group.add_argument('--modifyAccountList', action='store_const', const=True, help="mettre à jour plusieurs compte")
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
group.add_argument('--resetZimbraZimletAvailableZimlets', action='store_const', const=True, help="réinitialise la liste des zimlets pour un compte (utile pour hériter du paramètre de la classe de services)")
group.add_argument('--getCos', action='store_const', const=True, help="rechercher une classe de service")
group.add_argument('--getAllCos', action='store_const', const=True, help="rechercher toutes les classes de service du domaine")
group.add_argument('--getDomain', action='store_const', const=True, help="informations sur un domaine")
group.add_argument('--countObjects', action='store_const', const=True, help="compter les objets d'un domaine")
parser.add_argument('--type', metavar='userAccount', help="type d'objet à rechercher (userAccount, alias, dl ou calresource)")
group.add_argument('--getResource', action='store_const', const=True, help="rechercher une resource")
group.add_argument('--getAllResources', action='store_const', const=True, help="rechercher toutes les resources")
group.add_argument('--deleteResource', action='store_const', const=True, help="Supprimer une resource")
group.add_argument('--modifyResource', action='store_const', const=True, help="Modifier une resource")
group.add_argument('--createResource', action='store_const', const=True, help="Créer une resource")

# Requêtes sur les groupes
group.add_argument( '--getAllGroups', action = 'store_true' ,
    help = 'Afficher la liste des groupes et listes de distribution' )
group.add_argument( '--getGroup' , action = 'store_true' ,
    help = 'Rechercher un groupe / une liste de distribution' )
group.add_argument( '--getSendAsGroup' , action = 'store_true' ,
    help = '''Lister les l’ensemble des comptes pouvant utiliser l’adresse
              mail du groupe en adresse d’expédition.''' )
# Opérations sur les groupes
group.add_argument( '--createGroup' , action = 'store_true' ,
    help = '''Créer un groupe / une liste de distribution.''' )
group.add_argument( '--createGroupExt', action = 'store_true' ,
    help = '''Créer un groupe / une liste de distribution en spécifiant les
              paramètres via -f ou --jsonData''' )
group.add_argument( '--deleteGroup' , action = 'store_true' ,
    help = '''Supprimer un groupe / une liste de distribution.''' )
group.add_argument( '--addGroupAlias' , action = 'store_true' ,
    help = '''Ajoute des alias à un groupe / une liste de distribution.''' )
group.add_argument( '--removeGroupAlias' , action = 'store_true' ,
    help = '''Supprime des alias à un groupe / une liste de distribution.''' )
group.add_argument( '--setGroupAliases' , action = 'store_true' ,
    help = '''Modifie les alias à un groupe / une liste de distribution.''' )
group.add_argument( '--addGroupMember' , action = 'store_true' ,
    help = '''Ajoute des membres à un groupe / une liste de distribution.''' )
group.add_argument( '--removeGroupMember' , action = 'store_true' ,
    help = '''Supprime des membres d'un groupe / d'une liste de
              distribution.''' )
group.add_argument( '--setGroupMembers' , action = 'store_true' ,
    help = '''Modifie les membres d'un groupe / d'une liste de
              distribution.''' )
group.add_argument( '--addGroupSender' , action = 'store_true' ,
    help = '''Ajoute des autorisations d'utilisation de l'adresse du groupe ou
              de la liste de distribution par des comptes.''' )
group.add_argument( '--removeGroupSender' , action = 'store_true' ,
    help = '''Supprime des autorisations d'utilisation de l'adresse du groupe ou
              de la liste de distribution par des comptes.''' )
group.add_argument( '--setGroupSenders' , action = 'store_true' ,
    help = '''Modifie les autorisations d'utilisation de l'adresse du groupe ou
              de la liste de distribution par des comptes.''' )
group.add_argument('--addRootShare', action='store_true',
                   help='''Ajouter un partage root d'une boites de service à un ou plusieurs utilisateurs''')
args = vars(parser.parse_args())

# Connexion au BSS
try:
    bss = BSSConnexion()
    if args['bssUrl']:
        bss.url = args['bssUrl']
    bss.setDomainKey(listDomainKey={args['domain']: args['domainKey']})

except Exception as err:
    print("Echec de connexion : %s" % err)
    sys.exit(2)

if args['getAllAccounts'] == True:
    action_args = {
            'domain': args[ 'domain' ] ,
            'limit': args[ 'limit' ] ,
            'offset': args[ 'offset' ] ,
            'attrs': args[ 'attrs' ] ,
    }
    if args[ 'ldapQuery' ]:
        action_args[ 'ldapQuery' ] = args[ 'ldapQuery' ]

    try:
        all_accounts = AccountService.getAllAccounts( **action_args )
    except Exception as err:
        raise err

    print("%d comptes retournés :" % len(all_accounts))
    for account in all_accounts:
        print("Compte %s :" % account.name)
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
        print("Informations sur le compte %s :" % account.name)
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

elif args['resetZimbraZimletAvailableZimlets'] == True:

    emailList = []
    if args['email']:
        emailList.append(args['email'])
    else:
        emailList = []
        for email in sys.stdin:
            if not re.search(r'@', email):
                continue
            emailList.append(email.rstrip())

    countDone = 0
    for email in emailList:

        try:
            account = AccountService.getAccount(email)

        except Exception as err:
            print("Echec d'exécution pour compte %s : %s" % (email, err))
            continue

        try:
            account.resetZimbraZimletAvailableZimlets()
            AccountService.modifyAccount(account)
            countDone = countDone + 1

        except Exception as err:
            print("Echec d'exécution pour compte %s : %s" % (email, err))
            continue

    print("Les zimlets ont été réinitialisées pour les %d comptes ; les zimlets de la classe de services s'appliquent maintenant" % countDone)


elif args['restorePreDeleteAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    try:
        AccountService.restorePreDeleteAccount(args['email'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été rétabli" % args['email'])

elif args['createAccountExt'] == True:

    if not args[ 'userPassword' ]:
        print("Argument '--userPassword' manquant")
        sys.exit(1)

    # Objet du compte, éventuellement lu depuis un fichier JSON
    if args['jsonData']:
        account = importJsonAccount( args[ 'jsonData' ].name )
    else:
        account = Account( None )

    if args[ 'field' ]:
        account.fillAccount({
                arg[0] : arg[1] for arg in args[ 'field' ]
            } , allowNameChange = True)

    try:
        nAccount = AccountService.createAccountExt( account ,
                args[ 'userPassword' ] )
    except ( NameException , ServiceException , DomainException ) as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print( "Le compte %s a été créé" % nAccount.name )
    print( nAccount.showAttr( ) )

elif args['createAccount'] == True:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['userPassword']:
        raise Exception("Missing 'userPassword' argument")

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
        account = importJsonAccount(args['jsonData'].name)

    except Exception as err:
        print("Echec chargement fichier JSON %s : %s" % (args['jsonData'], err))
        sys.exit(2)

    try:
        AccountService.modifyAccount(account=account)

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Le compte %s a été mis à jour" % args['email'])

elif args['modifyAccountList'] == True:

    if not args['field']:
        raise Exception("Missing 'field' arguments")

    emailList = []
    for email in sys.stdin:
       if not re.search(r'@', email):
           continue
       emailList.append(email.rstrip())

    #print("Email: %s" % ','.join(emailList))

    for email in emailList:
        try:
            account = AccountService.getAccount(email)

        except Exception as err:
            print("Echec d'exécution pour le compte %s : %s" % (email,err))
            continue

        if not account:
            print("Compte %s non trouvé" % email)
            continue

        for field in args['field']:
            setattr(account, field[0], field[1])

        try:
            AccountService.modifyAccount(account=account)

        except Exception as err:
            print("Echec d'exécution : %s" % err)
            sys.exit(2)

        print("Le compte %s a été mis à jour" % email)

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

elif args['getCos'] == True:

    if not args['cosName']:
        raise Exception("Missing 'cosName' argument")

    try:
        cos = COSService.getCOS(args['domain'], args['cosName'])

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    if args['asJson']:
        print(json.dumps(cos.__dict__, sort_keys=True, indent=4))

    else:
        print("Informations sur la classe de service %s :" % cos.name)
        print(cos.showAttr())

elif args['getAllCos'] == True:
    try:
        all_cos = COSService.getAllCOS( args[ 'domain' ] )
    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("%d classes de service retournés :" % len(all_cos))
    for cos in all_cos:
        print("Classe de service %s :" % cos.name)
        print(cos.showAttr())

elif args['getDomain'] == True:
    try:
        domain = DomainService.getDomain( args[ 'domain' ] )
    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)
    domain_parsed = json.loads(json.dumps(domain))

    if not args['asJson']:
        print("Informations sur le domaine %s :" % args['domain'])

    print(json.dumps(domain_parsed, sort_keys=True, indent=4))

elif args['countObjects'] == True:

    if not args['type']:
        raise Exception("Missing 'type' argument")

    try:
        count = DomainService.countObjects(args['domain'], args['type'])
    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Nombre d'objets de type %s dans le domaine %s : %s" % (args['type'], args['domain'], count))


elif args[ 'getAllGroups' ]:
    data = {
        'domain' : args[ 'domain' ] ,
        'limit'  : args[ 'limit' ] ,
    }

    try:
        all_groups = GroupService.getAllGroups( **data )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )

    print( "{} groupes retournés".format( len( all_groups ) ) )
    if 'fullData' in args and args[ 'fullData' ]:
        print( 'Récupération des informations complètes...' )
        try:
            all_groups = [ GroupService.getGroup( g.name , full_info = True )
                                for g in all_groups ]
        except Exception as err:
            print( "Echec d'exécution : {}".format( repr( err ) ) )
            sys.exit( 2 )

    print( )
    for group in all_groups:
        print( "Groupe {} : ".format( group.name ) )
        print( group.showAttr( ) )
        print( )

elif args[ 'getGroup' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        data = { 'name' : args[ 'email' ] }
        if 'fullData' in args:
            data[ 'full_info' ] = args[ 'fullData' ]
        group = GroupService.getGroup( **data )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    if group is None:
        print( "Groupe {} non trouvé".format( args[ 'email' ] ) )
    else:
        print( group.showAttr( ) )

elif args[ 'getSendAsGroup' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        senders = GroupService.getSendAsGroup( args[ 'email' ] )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    if senders is None:
        print( "Groupe {} non trouvé".format( args[ 'email' ] ) )
    elif not senders:
        print( "Pas d'utilisateurs autorisés" )
    else:
        print( "Utilisateurs autorisés: {}".format( ', '.join( senders ) ) )

elif args[ 'createGroup' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        GroupService.createGroup( args[ 'email' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        raise err
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'createGroupExt' ]:
    try:
        # Objet du compte, éventuellement lu depuis un fichier JSON
        if args[ 'jsonData' ]:
            group = Group.from_json( args[ 'jsonData' ] , is_file = True )
        else:
            group = Group( )

        if args[ 'field' ]:
            group.from_dict({
                    arg[ 0 ] : arg[ 1 ]
                        for arg in args[ 'field' ]
                } , allow_name = True )

        GroupService.createGroup( group )
        group = GroupService.getGroup( group.name , full_info = True )
    except Exception as err:
        raise err
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'deleteGroup' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        GroupService.deleteGroup( args[ 'email' ] )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( "Groupe {} supprimé".format( args[ 'email' ] ) )

elif args[ 'addGroupAlias' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'alias' ]:
            raise Exception( "Argument 'alias' manquant" )
        GroupService.addGroupAliases( args[ 'email' ] , args[ 'alias' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'removeGroupAlias' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'alias' ]:
            raise Exception( "Argument 'alias' manquant" )
        GroupService.removeGroupAliases( args[ 'email' ] , args[ 'alias' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'setGroupAliases' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'alias' ]:
            args[ 'alias' ] = ( )
        GroupService.updateGroupAliases( args[ 'email' ] , args[ 'alias' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        raise err
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'addGroupMember' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'member' ]:
            raise Exception( "Argument 'member' manquant" )
        GroupService.addGroupMembers( args[ 'email' ] , args[ 'member' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'removeGroupMember' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'member' ]:
            raise Exception( "Argument 'member' manquant" )
        GroupService.removeGroupMembers( args[ 'email' ] , args[ 'member' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'setGroupMembers' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'member' ]:
            args[ 'member' ] = ( )
        GroupService.updateGroupMembers( args[ 'email' ] , args[ 'member' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        raise err
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'addGroupSender' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'sender' ]:
            raise Exception( "Argument 'sender' manquant" )
        GroupService.addGroupSenders( args[ 'email' ] , args[ 'sender' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'removeGroupSender' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'sender' ]:
            raise Exception( "Argument 'sender' manquant" )
        GroupService.removeGroupSenders( args[ 'email' ] , args[ 'sender' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'setGroupSenders' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        if not args[ 'sender' ]:
            args[ 'sender' ] = ( )
        GroupService.updateGroupSenders( args[ 'email' ] , args[ 'sender' ] )
        group = GroupService.getGroup( args[ 'email' ] , full_info = True )
    except Exception as err:
        raise err
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( group.showAttr( ) )

elif args[ 'addRootShare' ]:
    if not args['email']:
        raise Exception("Argument 'email' manquant")
    if not args['recipients']:
        raise Exception("Argument 'recipients' manquant")
    if not args['rights']:
        raise Exception("Argument 'rights' manquant")

    try:
        PartageService.addRootShare(args['email'], [args['recipients']], [args['rights']])
    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("Partage de la boîte %s avec %s mise en place avec les droits %s" % (args['email'],args['recipients'],args['rights']))

elif args[ 'getResource' ]:
    if not args['email']:
        raise Exception("Argument 'email' manquant")

    try:
        data = { 'name' : args[ 'email' ] }
        resource = ResourceService.getResource( **data )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    if resource is None:
        print( "Groupe {} non trouvé".format( args[ 'email' ] ) )
    else:
        print( resource.showAttr( ) )

elif args[ 'getAllResources' ]:
    data = {
        'domain' : args[ 'domain' ] ,
        'limit'  : args[ 'limit' ]
    }

    try:
        all_resources = ResourceService.getAllResources( **data )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )

    print( "{} groupes retournés".format( len( all_resources ) ) )

    print( )
    for resource in all_resources:
        print( "Resource {} : ".format( resource.name ) )
        print( resource.showAttr( ) )
        print( )

elif args[ 'deleteResource' ]:
    try:
        if not args[ 'email' ]:
            raise Exception( "Argument 'email' manquant" )
        ResourceService.deleteResource( args[ 'email' ] )
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )
    print( "Ressource {} supprimé".format( args[ 'email' ] ) )

elif args['createResource']:

    if not args['email']:
        raise Exception("Missing 'email' argument")

    if not args['userPassword']:
        raise Exception("Missing 'userPassword' argument")

    if not args['zimbraCalResType']:
        raise Exception("Missing 'zimbraCalResType' argument")

    if not args['displayName']:
        raise Exception("Missing 'displayName' argument")

    try:
        ResourceService.createResource(name=args['email'], zimbraCalResType=args['zimbraCalResType'],displayName=args['displayName'],password=args['userPassword'], )

    except Exception as err:
        print("Echec d'exécution : %s" % err)
        sys.exit(2)

    print("La Ressource %s a été créé" % args['email'])

elif args[ 'modifyResource' ]:

    if not args['field']:
        raise Exception("Missing 'field' arguments")

    if not args['email']:
        raise Exception("Argument 'email' manquant")

    try:
        resource = ResourceService.getResource(args['email'])

        for field in args['field']:
            setattr(resource, field[0], field[1])
    except Exception as err:
        print( "Echec d'exécution : {}".format( repr( err ) ) )
        sys.exit( 2 )

    try:
        ResourceService.modifyResource(resource)
    except Exception as err:
        print("Echec d'exécution 1 : {}".format(repr(err)))
        sys.exit(2)
    print( "Ressource {} bien Modifié".format( resource.name ) )

else:
    print("Aucune opération à exécuter")
