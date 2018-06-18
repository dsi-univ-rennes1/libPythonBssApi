# -*-coding:utf-8 -*
from lib_Partage_BSS.models.Group import Group
from .GlobalService import callMethod
from lib_Partage_BSS import services , utils
from lib_Partage_BSS.exceptions import ( NameException , DomainException ,
                                         ServiceException )


#-------------------------------------------------------------------------------
# Opérations d'interrogation


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


#-------------------------------------------------------------------------------
# Création & suppression

def createGroup( name_or_group ):
    is_group = isinstance( name_or_group , Group )
    if is_group:
        if name_or_group.name is None:
            raise NameException( "L'adresse mail n'est pas renseignée" )
        data = name_or_group.to_bss( )
    else:
        if not isinstance( name_or_group , str ):
            raise TypeError
        data = { 'name' : name_or_group }

    if not utils.checkIsMailAddress( data[ 'name' ] ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( n ) )

    domain = services.extractDomain( data[ 'name' ] )
    response = callMethod( domain , 'CreateGroup' , data )
    if not utils.checkResponseStatus( response[ 'status' ] ):
        raise ServiceException( response[ 'status' ] , response[ 'message' ] )

    if not is_group:
        return
    if name_or_group.has_aliases:
        addGroupAliases( name_or_group.name , name_or_group.aliases )
    if name_or_group.has_members:
        addGroupMembers( name_or_group.name , name_or_group.members )
    if name_or_group.has_senders:
        addGroupSenders( name_or_group.name , name_or_group.senders )

def deleteGroup( name_or_group ):
    if isinstance( name_or_group , Group ):
        if name_or_group.name is None:
            raise NameException( "L'adresse mail n'est pas renseignée" )
        data = { 'name' : name_or_group.name }
    else:
        if not isinstance( name_or_group , str ):
            raise TypeError
        data = { 'name' : name_or_group }

    if not utils.checkIsMailAddress( data[ 'name' ] ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( n ) )

    domain = services.extractDomain( data[ 'name' ] )
    response = callMethod( domain , 'DeleteGroup' , data )
    if not utils.checkResponseStatus( response[ 'status' ] ):
        raise ServiceException( response[ 'status' ] , response[ 'message' ] )


#-------------------------------------------------------------------------------
# Opération de modification

def modifyGroup( group ):
    response = callMethod( services.extractDomain( group.name ) ,
            'ModifyGroup' , group.to_bss( ) )
    if not utils.checkResponseStatus( response[ 'status' ] ):
        raise ServiceException( response[ 'status' ] , response[ 'message' ] )

#-------------------------------------------------------------------------------

def _group_set_op( name_or_group , entries , f_name , op_name ):
    if isinstance( entries , str ):
        entries = [ entries ]
    else:
        entries = list( entries )

    if isinstance( name_or_group , Group ):
        name = name_or_group.name
    else:
        name = name_or_group

    for n in ( name , *entries ):
        if not utils.checkIsMailAddress( n ):
            raise NameException(
                    "L'adresse mail {} n'est pas valide".format( n ) )

    domain = services.extractDomain( name )
    if '[]' in f_name:
        entries = [entries]

    for entry in entries:
        data = {
                'name' : name ,
                f_name : entry ,
            }
        print( domain , op_name , repr( data ) )
        response = callMethod( domain , op_name , data )
        if not utils.checkResponseStatus( response[ 'status' ] ):
            raise ServiceException( response[ 'status' ] ,
                    response[ 'message' ] )

def _group_diff_op( name_or_group , new_values , a_name , f_name ,
            add_op_name , rem_op_name ):
    if isinstance( name_or_group , Group ):
        group = name_or_group
    else:
        group = getGroup( name_or_group , full_info = 'senders' == a_name )

    if isinstance( new_values , str ):
        nv_set = set( ( new_values , ) )
    else:
        nv_set = set( new_values )
    grp_set = getattr( group , '{}_set'.format( a_name ) )

    rem = grp_set - nv_set
    if rem: _group_set_op( group , rem , f_name , rem_op_name )

    add = nv_set - grp_set
    if add: _group_set_op( group , add , f_name , add_op_name )


#-------------------------------------------------------------------------------

def addGroupAliases( name_or_group , aliases ):
    _group_set_op( name_or_group , aliases ,
            'alias' , 'AddDistributionListAlias' )

def removeGroupAliases( name_or_group , aliases ):
    _group_set_op( name_or_group , aliases ,
            'alias' , 'RemoveDistributionListAlias' )

def updateGroupAliases( name_or_group , new_aliases ):
    _group_diff_op( name_or_group , new_aliases , 'aliases' , 'alias' ,
            'AddDistributionListAlias' , 'RemoveDistributionListAlias' )

#-------------------------------------------------------------------------------

def addGroupMembers( name_or_group , members ):
    _group_set_op( name_or_group , members ,
            'members[]' , 'AddGroupMembers' )

def removeGroupMembers( name_or_group , members ):
    _group_set_op( name_or_group , members ,
            'members[]' , 'RemoveGroupMembers' )

def updateGroupMembers( name_or_group , new_members ):
    _group_diff_op( name_or_group , new_members , 'members' , 'members[]' ,
            'AddGroupMembers' , 'RemoveGroupMembers' )

#-------------------------------------------------------------------------------

def addGroupSenders( name_or_group , senders ):
    _group_set_op( name_or_group , senders ,
            'account' , 'AddSendAsGroup' )

def removeGroupSenders( name_or_group , senders ):
    _group_set_op( name_or_group , senders ,
            'account' , 'DeleteSendAsGroup' )

def updateGroupSenders( name_or_group , new_senders ):
    _group_diff_op( name_or_group , new_senders , 'senders' , 'account' ,
            'AddSendAsGroup' , 'DeleteSendAsGroup' )
