# -*-coding:utf-8 -*
from lib_Partage_BSS.models.Group import Group
from .GlobalService import callMethod
from lib_Partage_BSS import services , utils
from lib_Partage_BSS.exceptions import ( NameException , DomainException ,
                                         ServiceException )


def getAllGroups( domain , limit = 100 , offset = 0 ):
    data = {
        'limit'  : limit ,
        'offset' : offset ,
    }

    response = callMethod( domain , 'GetAllGroups' , data )
    if not utils.checkResponseStatus( response[ 'status' ] ):
        raise ServiceException( response[ 'status' ] , response[ 'message' ] )

    if len( response[ 'groups' ] ) <= 1:
        return []

    groups = response[ 'groups' ][ 'group' ]
    if isinstance( groups , list ):
        return [ Group.from_bss( e ) for e in groups ]
    return Group.from_bss( groups )


def getGroup( name , full_info = False ):
    if not utils.checkIsMailAddress( name ):
        raise NameException( "L'adresse mail {} n'est pas valide".format(
                name ) )

    data = { 'name' : name }
    domain = services.extractDomain( name )
    response = callMethod( domain , 'GetGroup' , data )

    if utils.checkResponseStatus( response[ 'status' ] ):
        group = Group.from_bss( response[ 'group' ] )
        if full_info:
            getSendAsGroup( group )
        return group
    if 'no such distribution list' in response[ 'message' ]:
        return None
    raise ServiceException( response[ 'status' ] , response[ 'message' ] )


def getSendAsGroup( name_or_group ):
    if isinstance( name_or_group , Group ):
        name = name_or_group.name
        group = name_or_group
    else:
        name = name_or_group
        if not utils.checkIsMailAddress( name ):
            raise NameException( "L'adresse mail {} n'est pas valide".format(
                    name ) )
        group = Group( name )

    data = { 'name' : name }
    domain = services.extractDomain( name )
    response = callMethod( domain , 'GetSendAsGroup' , data )

    if utils.checkResponseStatus( response[ 'status' ] ):
        return group.senders_from_bss( response )
    if 'no such distribution list' in response[ 'message' ]:
        return None
    raise ServiceException( response[ 'status' ] , response[ 'message' ] )
