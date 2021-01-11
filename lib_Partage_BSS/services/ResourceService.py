# -*-coding:utf-8 -*
"""
Module contenant les méthodes permettant d'appeler les services de l'API BSS
concernant les resources.
"""
import re

from lib_Partage_BSS.models.Resource import Resource
from .GlobalService import callMethod, checkResponseStatus
from lib_Partage_BSS import services , utils
from lib_Partage_BSS.exceptions import NameException, DomainException, ServiceException, TmpServiceException, NotFoundException



#-------------------------------------------------------------------------------
# Opérations d'interrogation

def getAllResources( domain , limit = 100 , offset = 0 ):
    """
    Lit la liste de toutes les resources depuis le serveur Partage.

    :param domain: le domaine de la recherche
    :param limit: le nombre maximal d'entrées à renvoyer
    :param offset: l'index du premier élément à renvoyer

    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide

    :return: la liste des resources, sous la forme d'instances du modèle.
    """
    data = {
        'limit'  : limit ,
        'offset' : offset ,
        'sortby' : 'mail'
    }

    response = callMethod( domain , 'GetAllResources' , data )
    try:
        checkResponseStatus(response)
    except NotFoundException:
        return None

    # Attention : xmljson retourne un dictionnaire contenant une entrée également par attribut XML
    # Donc il y a une entrée pour l'attribut "type" de "<groups type="array">"
    if len( response[ 'resources' ] ) == 1:
        return []

    resources = response[ 'resources' ][ 'resource' ]
    if isinstance( resources , list ):
        return [ Resource.from_bss( e ) for e in resources ]
    else:
        return [ Resource.from_bss(resources) ]


def getResource( name ):
    """
    Lit les informations concernant une ressource.

    :param name: l'adresse mail de la resource

    :raises NameException: l'adresse de groupe spécifiée est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide

    :return: la Ressource, sous la forme d'une instance du modèle, ou bien None \
            si aucune resource ne correspond au nom spécifié
    """
    if not utils.checkIsMailAddress( name ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( name ) )
    data = { 'name' : name }
    domain = services.extractDomain( name )
    response = callMethod( domain , 'GetResource' , data )
    try:
        checkResponseStatus(response)
    except NotFoundException:
        return None
    resource = response[ 'resource' ]
    return Resource.from_bss( resource )

#-------------------------------------------------------------------------------
# Création & suppression

def createResource( name, displayName, userPassword=None, zimbraCalResType="Location", password=None, resource=None ):
    """
    Crée une ressource en se basant sur une instance du
    modèle, ou simplement en utilisant un nom.

    :param name_or_resource: le nom de la resource à créer, ou bien une instance du \
            modèle contenant les informations initiales au sujet de la resource.

    :raises TypeError: si le paramètre n'est ni un nom ni une instance du modèle
    :raises NameError: si l'adresse de la ressource à créer est invalide
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """

    if not utils.checkIsMailAddress(name):
        raise NameException("L'adresse mail " + name + " n'est pas valide")

    # Les attributs issus de l'objet account
    data = {}
    if resource is not None:
        data = resource.toData()

    # Les attributs obligatoires
    if password is not None:
        data.update({'name': name,
                     'password': password,
                     'zimbraCalResType': zimbraCalResType,
                     'zimbraAccountStatus': "active",
                     'displayName': displayName
                     })
    else:
        if not re.search(r'^\{\S+\}', userPassword):
            raise NameException(
                "Le format de l'empreinte du mot de passe n'est pas correcte ; format attendu : {algo}empreinte")
        data.update({'name': name,
                'userPassword': userPassword,
                'zimbraCalResType': zimbraCalResType,
                'zimbraAccountStatus': "active",
                'displayName': displayName
                })
    if not utils.checkIsMailAddress( data[ 'name' ] ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( name ) )

    domain = services.extractDomain( data[ 'name' ] )
    response = callMethod( domain , 'CreateResource' , data )
    checkResponseStatus(response)

    return getResource(name)

def deleteResource( name_or_resource ):
    """
    Supprime une ressource.

    :param name_or_resource: le nom de la resource, ou bien l'instance de modèle \
            correspondante.

    :raises NameException: l'adresse de la resource spécifiée est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """
    if isinstance( name_or_resource , Resource ):
        if name_or_resource.name is None:
            raise NameException( "L'adresse mail n'est pas renseignée" )
        data = { 'name' : name_or_resource.name }
    else:
        if not isinstance( name_or_resource , str ):
            raise TypeError
        data = { 'name' : name_or_resource }

    if not utils.checkIsMailAddress( data[ 'name' ] ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( name_or_resource ) )

    domain = services.extractDomain( data[ 'name' ] )
    response = callMethod( domain , 'DeleteResource' , data )
    checkResponseStatus( response)

#-------------------------------------------------------------------------------
# Opération de modification

def modifyResource( resource ):
    """
    Modifie les informations concernant une ressource.

    :param resource: l'instance du modèle contenant les nouvelles informations \
            ainsi que l'adresse de la ressource à modifier

    :raises NameException: l'adresse de la ressource spécifiée est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """
    response = callMethod( services.extractDomain( resource.name ) ,
            'ModifyResource' , resource.toData( ) )
    checkResponseStatus( response)
