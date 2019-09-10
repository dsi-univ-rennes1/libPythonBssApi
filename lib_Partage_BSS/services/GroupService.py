# -*-coding:utf-8 -*
"""
Module contenant les méthodes permettant d'appeler les services de l'API BSS
concernant les groupes et listes de distribution.
"""

from lib_Partage_BSS.models.Group import Group
from .GlobalService import callMethod, checkResponseStatus
from lib_Partage_BSS import services , utils
from lib_Partage_BSS.exceptions import NameException, DomainException, ServiceException, TmpServiceException, NotFoundException



#-------------------------------------------------------------------------------
# Opérations d'interrogation

def getAllGroups( domain , limit = 100 , offset = 0 ):
    """
    Lit la liste de tous les groupes depuis le serveur Partage.

    :param domain: le domaine de la recherche
    :param limit: le nombre maximal d'entrées à renvoyer
    :param offset: l'index du premier élément à renvoyer

    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide

    :return: la liste des groupes, sous la forme d'instances du modèle.
    """
    data = {
        'limit'  : limit ,
        'offset' : offset ,
    }

    response = callMethod( domain , 'GetAllGroups' , data )
    checkResponseStatus( response)

    # Attention : xmljson retourne un dictionnaire contenant une entrée également par attribut XML
    # Donc il y a une entrée pour l'attribut "type" de "<groups type="array">"
    if len( response[ 'groups' ] ) == 1:
        return []

    groups = response[ 'groups' ][ 'group' ]
    if isinstance( groups , list ):
        return [ Group.from_bss( e ) for e in groups ]
    else:
        return [ Group.from_bss(groups) ]


def getGroup( name , full_info = False ):
    """
    Lit les informations concernant un groupe.

    :param name: l'adresse mail du groupe ou de la liste de distribution
    :param full_info: une requête additionnelle permettant de lister \
            les expéditeurs autorisés doit-elle être effectuée ?

    :raises NameException: l'adresse de groupe spécifiée est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide

    :return: le groupe, sous la forme d'une instance du modèle, ou bien None \
            si aucun groupe ne correspond au nom spécifié
    """
    if not utils.checkIsMailAddress( name ):
        raise NameException( "L'adresse mail {} n'est pas valide".format(
                name ) )

    data = { 'name' : name }
    domain = services.extractDomain( name )
    response = callMethod( domain , 'GetGroup' , data )

    try:
        checkResponseStatus(response)
    except NotFoundException:
        return None

    group = Group.from_bss( response[ 'group' ] )
    if full_info:
        getSendAsGroup( group )
    return group


def getSendAsGroup( name_or_group ):
    """
    Lit la liste des utilisateurs autorisés à expédier du mail en utilisant
    l'adresse d'un groupe comme expéditeur.

    :param name_or_group: l'adresse d'un groupe ou l'instance correspondant au \
            groupe pour lequel on veut lire la liste des autorisations. Si une \
            instance est passée, son champ 'senders' sera mis à jour

    :raises NameException: l'adresse de groupe spécifiée est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide

    :return: l'ensemble des utilisateurs autorisés, ou None si le groupe n'a \
            pas été trouvé
    """
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

    try:
        checkResponseStatus(response)
    except NotFoundException:
        return None

    return group.senders_from_bss(response)


#-------------------------------------------------------------------------------
# Création & suppression

def createGroup( name_or_group ):
    """
    Crée un groupe ou une liste de distribution en se basant sur une instance du
    modèle, ou simplement en utilisant un nom.

    Si une instance est utilisée et que des alias, des membres ou des
    autorisations d'expéditions sont présents dans l'instance, ils seront
    ajoutés au groupe sur Partage après sa création.

    :param name_or_group: le nom du groupe à créer, ou bien une instance du \
            modèle contenant les informations initiales au sujet du groupe.

    :raises TypeError: si le paramètre n'est ni un nom ni une instance du modèle
    :raises NameError: si l'adresse du groupe à créer est invalide, ou si \
            l'une des autres informations de ce type (alias, membres, \
            autorisation) est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """
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
    checkResponseStatus( response)

    if not is_group:
        return
    if name_or_group.has_aliases:
        addGroupAliases( name_or_group.name , name_or_group.aliases )
    if name_or_group.has_members:
        addGroupMembers( name_or_group.name , name_or_group.members )
    if name_or_group.has_senders:
        addGroupSenders( name_or_group.name , name_or_group.senders )

def deleteGroup( name_or_group ):
    """
    Supprime un groupe.

    :param name_or_group: le nom du groupe, ou bien l'instance de modèle \
            correspondante.

    :raises NameException: l'adresse de groupe spécifiée est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """
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
    checkResponseStatus( response)


#-------------------------------------------------------------------------------
# Opération de modification

def modifyGroup( group ):
    """
    Modifie les informations concernant un groupe. Les membres, alias et
    autorisations ne sont pas affectés.

    :param group: l'instance du modèle contenant les nouvelles informations \
            ainsi que l'adresse du groupe à modifier

    :raises NameException: l'adresse de groupe spécifiée est incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """
    response = callMethod( services.extractDomain( group.name ) ,
            'ModifyGroup' , group.to_bss( ) )
    checkResponseStatus( response)

#-------------------------------------------------------------------------------

def _group_set_op( name_or_group , entries , f_name , op_name ):
    """
    Fonction interne utilisée pour effectuer les ajouts ou suppressions sur les
    listes de membres, d'alias et d'autorisations d'expédition d'un groupe.

    :param name_or_group: le nom du groupe à modifier, ou l'instance du modèle \
            correspondante
    :param entries: l'entrée ou les entrées à ajouter ou supprimer
    :param f_name: le nom du champ tel qu'il doit être envoyé à l'API BSS; si \
            le nom finit par '[]', toutes les informations seront envoyées \
            en un seul appel
    :param op_name: le nom de la méthode distante à utiliser

    :raises TypeError: le groupe n'est ni un nom, ni une instance de modèle
    :raises NameException: l'adresse de groupe ou l'une des entrées est \
            incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """
    if isinstance( entries , str ):
        entries = [ entries ]
    else:
        entries = list( entries )

    if isinstance( name_or_group , Group ):
        name = name_or_group.name
    else:
        if not isinstance( name_or_group , str ):
            raise TypeError
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
        response = callMethod( domain , op_name , data )
        checkResponseStatus( response)


def _group_diff_op( name_or_group , new_values , a_name , f_name ,
            add_op_name , rem_op_name ):
    """
    Fonction interne utilisée pour effectuer les modifications sur les listes de
    membres, d'alias et d'autorisations d'expédition d'un groupe.

    :param name_or_group: le nom du groupe à modifier, ou l'instance du modèle \
            correspondante; si seul le nom est passé, getGroup() sera appelée
    :param new_values: la nouvelle liste des entrées pour le champ concerné
    :param a_name: le nom du champ dans l'instance de modèle
    :param f_name: le nom du champ tel qu'il doit être envoyé à l'API BSS; si \
            le nom finit par '[]', toutes les informations seront envoyées \
            en un seul appel
    :param add_op_name: le nom de la méthode distante à utiliser pour ajouter \
            des entrées
    :param rem_op_name: le nom de la méthode distante à utiliser pour \
            supprimer des entrées

    :raises TypeError: le groupe n'est ni un nom, ni une instance de modèle
    :raises NameException: l'adresse de groupe ou l'une des entrées est \
            incorrecte
    :raises ServiceException: la requête vers l'API a echoué
    :raises DomainException: le domaine n'est pas valide
    """
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
    """
    Ajoute des alias à un groupe ou une liste de distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param aliases: un alias sous la forme d'une chaîne, ou une collection \
            d'alias
    """
    _group_set_op( name_or_group , aliases ,
            'alias' , 'AddDistributionListAlias' )

def removeGroupAliases( name_or_group , aliases ):
    """
    Supprime des alias d'un groupe ou d'une liste de distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param aliases: un alias sous la forme d'une chaîne, ou une collection \
            d'alias
    """
    _group_set_op( name_or_group , aliases ,
            'alias' , 'RemoveDistributionListAlias' )

def updateGroupAliases( name_or_group , new_aliases ):
    """
    Met à jour les alias d'un groupe ou d'une liste de distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param aliases: un alias sous la forme d'une chaîne, ou une collection \
            d'alias
    """
    _group_diff_op( name_or_group , new_aliases , 'aliases' , 'alias' ,
            'AddDistributionListAlias' , 'RemoveDistributionListAlias' )

#-------------------------------------------------------------------------------

def addGroupMembers( name_or_group , members ):
    """
    Ajoute des membres à un groupe ou une liste de distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param members: un membre sous la forme d'une chaîne, ou une collection \
            de membres
    """
    _group_set_op( name_or_group , members ,
            'members[]' , 'AddGroupMembers' )

def removeGroupMembers( name_or_group , members ):
    """
    Supprime des membres d'un groupe ou d'une liste de distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param members: un membre sous la forme d'une chaîne, ou une collection \
            de membres
    """
    _group_set_op( name_or_group , members ,
            'members[]' , 'RemoveGroupMembers' )

def updateGroupMembers( name_or_group , new_members ):
    """
    Met à jour les membres d'un groupe ou d'une liste de distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param members: un membre sous la forme d'une chaîne, ou une collection \
            de membres
    """
    _group_diff_op( name_or_group , new_members , 'members' , 'members[]' ,
            'AddGroupMembers' , 'RemoveGroupMembers' )

#-------------------------------------------------------------------------------

def addGroupSenders( name_or_group , senders ):
    """
    Ajoute des utilisateurs autorisés à un groupe ou une liste de distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param members: un utilisateur autorisé sous la forme d'une chaîne, ou une \
            collection d'utilisateurs autorisés
    """
    _group_set_op( name_or_group , senders ,
            'account' , 'AddSendAsGroup' )

def removeGroupSenders( name_or_group , senders ):
    """
    Supprime des utilisateurs autorisés d'un groupe ou d'une liste de
    distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param members: un utilisateur autorisé sous la forme d'une chaîne, ou une \
            collection d'utilisateurs autorisés
    """
    _group_set_op( name_or_group , senders ,
            'account' , 'DeleteSendAsGroup' )

def updateGroupSenders( name_or_group , new_senders ):
    """
    Met à jour les utilisateurs autorisés d'un groupe ou d'une liste de
    distribution.

    :param name_or_group: le nom du groupe, ou l'instance de modèle \
            correspondante
    :param members: un utilisateur autorisé sous la forme d'une chaîne, ou une \
            collection d'utilisateurs autorisés
    """
    _group_diff_op( name_or_group , new_senders , 'senders' , 'account' ,
            'AddSendAsGroup' , 'DeleteSendAsGroup' )
