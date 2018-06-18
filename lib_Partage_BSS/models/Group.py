# -*-coding:utf-8 -*
import json

from lib_Partage_BSS import utils
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.models.GlobalModel import GlobalModel


class Group( GlobalModel ):
    """
    Classe représentant un groupe ou une liste de distribution dans Partage.

    :ivar _description: description du groupe ou de la liste
    :ivar _displayName: nom d'affichage du groupe
    :ivar _zimbraDistributionListSendShareMessageToNewMembers: détermine \
            si la liste des partages devrait être envoyée par mail aux \
            nouveaux membres
    :ivar _zimbraHideInGal: masquer dans la GAL ?
    :ivar _zimbraMailStatus: ce groupe peut-il recevoir du mail? Si oui, \
            il s'agit d'une liste de distribution.
    :ivar _zimbraNotes: notes concernant le groupe ou la liste.
    :ivar _members: l'ensemble des adresses des membres du groupe ou \
            de la liste
    :ivar _senders: l'ensemble des comptes autorisés à envoyer du mail en \
            utilisant la liste comme adresse d'expédition
    :ivar _aliases: l'ensemble des alias de la liste
    """

    # Attributs utilisés dans {Create,Modify}Account
    ATTRIBUTES = (
            'description' , 'displayName' ,
            'zimbraDistributionListSendShareMessageToNewMembers' ,
            'zimbraHideInGal' , 'zimbraMailStatus' , 'zimbraNotes'
        )

    # Attributs synthétiques sous la forme d'ensembles
    SETS = ( 'members' , 'senders' , 'aliases' )

    def __init__( self , name = None ):
        if name is not None and not isinstance( name , str ):
            raise TypeError
        if name is not None and not utils.checkIsMailAddress( name ):
            raise NameException( "Adresse mail {} invalide".format( name ) )

        GlobalModel.__init__( self , name )

        for a in Group.ATTRIBUTES:
            setattr( self , '_{}'.format( a ) , None )
        self._members = set( )
        self._senders = set( )
        self._aliases = set( )

    #---------------------------------------------------------------------------

    @staticmethod
    def _get_set( output , data , name , sub = None ):
        """
        Récupère les données correspondant à un attribut de type ensemble depuis
        la réponse du serveur BSS.

        :param output: l'instance à mettre à jour
        :param data: les données reçues du serveur
        :param name: le nom du champ contenant la liste
        :param sub: le nom des éléments de la liste, s'ils diffèrent du nom \
                de celle-ci
        """
        if name not in data: return
        od = data[ name ]
        if sub is None:
            sub = name
        if sub in od:
            if isinstance( od[ sub ] , str ):
                output.add( od[ sub ] )
            else:
                output.update( od[ sub ] )

    @staticmethod
    def _from_bool( value , true_value , false_value , xform ):
        """
        Vérifie et retourne la valeur à utiliser pour un champ 'booléen' mais
        encodé sous la forme de chaînes.

        :param value: la nouvelle valeur du champ
        :param true_value: la chaîne correspondant à une valeur vraie
        :param false_value: la chaîne correspondant à une valeur fausse
        :param xform: une fonction qui transforme la chaîne d'entrée si \
                nécessaire

        :raises TypeError: la valeur n'est ni une chaîne ni un booléen, ou \
                sa valeur ne correspond pas à l'une des chaînes indiquées

        :return: la nouvelle valeur du champ
        """
        if value is None:
            return None
        v = None
        if isinstance( value , str ) and xform( value ) in ( true_value ,
                    false_value ):
            v = xform( value )
        elif isinstance( value , bool ):
            v = true_value if value else false_value
        if v is None:
            raise TypeError
        return v

    #---------------------------------------------------------------------------

    @staticmethod
    def from_bss( data ):
        """
        Crée une instance en se basant sur des données reçues du serveur
        Partage, soit via GetGroup soit via GetAllGroups. Dans le premier cas,
        tous les champs à l'exception de la liste des utilisateurs autorisés à
        expédier avec l'adresse du groupe seront mis à jour.

        :param data: les données du compte reçues depuis le serveur Partage

        :raises TypeError: un champ n'a pas le format attendu

        :return: l'instance de Group créée, avec ses champs renseignés
        """
        group = Group( data[ 'name' ] )
        group.from_dict( data )
        Group._get_set( group._members , data , 'members' , 'member' )
        Group._get_set( group._aliases , data , 'zimbraMailAlias' )
        return group

    def from_dict( self , data , allow_name = False ):
        """
        Met à jour les champs d'une instance à partir d'un dictionnaire. Seuls
        les attributs, et optionellement le nom, peuvent être modifiés par cette
        méthode.

        :param data: le dictionnaire à partir duquel on veut mettre à jour les \
                données
        :param allow_name: permettre la modification du champ 'name' à partir \
                du dictionnaire; si False, une entrée 'name' dans le \
                dictionnaire sera ignorée

        :raises TypeError: un champ n'a pas le format attendu
        """
        attrs = (
                ( 'name' , *Group.ATTRIBUTES ) if allow_name
                else Group.ATTRIBUTES
            )
        for a in attrs:
            if a in data:
                setattr( self , a , data[ a ] )

    def senders_from_bss( self , data ):
        """
        Remplace la liste des utilisateurs autorisés à expédier avec l'adresse
        de ce groupe à partir de données fournies par le serveur Partage.

        :param data: les données reçues du serveur Partage

        :return: l'ensemble des adresses autorisées
        """
        self._senders.clear( )
        Group._get_set( self._senders , data , 'accounts' , 'account' )
        return self.senders

    def to_bss( self ):
        """
        Génère un dictionnaire pouvant être utilisé pour créer ou modifier un
        groupe sur le serveur.

        :return: le dictionnaire contenant les attributs
        """
        rv = { }
        for a in ( 'name' , *Group.ATTRIBUTES ):
            value = getattr( self , a )
            if value is not None:
                rv[ a ] = value
        return rv

    #---------------------------------------------------------------------------

    @staticmethod
    def from_json( source , is_file = False ):
        """
        Génère une instance à partir de données au format JSON.

        :param source: la source des données à partir desquelles on doit créer \
                une instance. Il peut s'agir de source JSON ou bien d'un \
                fichier, en fonction de la valeur du paramètre is_file. Dans \
                le second cas, on peut passer aussi bien le chemin du fichier \
                qu'une instance (par exemple de file) permettant le chargement \
                du JSON.
        :param is_file: un booléen qui indique si le paramètre précédent est \
                un fichier (True) ou du source JSON (False).

        :raises TypeError: si certains des champs ont des types invalides
        :raises NameException: si l'adresse contenue dans le champ name, ou \
                l'une des adresses de membres, l'un des alias ou l'une des \
                entrées d'autorisation sont invalides

        :return: l'instance créée
        """
        if is_file:
            if isinstance( source , str ):
                with open( source ) as json_file:
                    data = json.load( json_file )
            else:
                data = json.load( source )
        else:
            data = json.loads( source )
        return Group.from_json_record( data )

    @staticmethod
    def from_json_record( record ):
        """
        Génère une instance à partir de données JSON décodées dans un
        dictionnaire Python.

        :param record: le dictionnaire dans lequel les information ont été \
                décodées

        :raises TypeError: si certains des champs ont des types invalides
        :raises NameException: si l'adresse contenue dans le champ name, ou \
                l'une des adresses de membres, l'un des alias ou l'une des \
                entrées d'autorisation sont invalides

        :return: l'instance créée
        """
        group = Group( record[ 'name' ] if 'name' in record else None )
        for a in Group.ATTRIBUTES:
            if a in record:
                setattr( group , a , record[ a ] )
        for s in Group.SETS:
            if s in record:
                bad_addr = set([ a for a in record[ s ]
                                    if not utils.checkIsMailAddress( a ) ])
                if not bad_addr:
                    getattr( group , '_{}'.format( s ) ).update( record[ s ] )
                    continue
                raise NameException( "Adresse(s) mail {} invalide(s)".format(
                            ', '.join( bad_addr ) ) )
        return group

    def to_json_record( self ):
        """
        Génère les données (sous la forme d'un dictionnaire Python) pour un
        enregistrement JSON décrivant l'instance.

        :return: un dictionnaire contenant les champs appropriés pour \
                sauvegarde au format JSON
        """
        rv = {
            a : getattr( self , a )
                for a in ( 'name' , *Group.ATTRIBUTES )
                if getattr( self , a ) is not None
        }
        rv.update({
            s : list( getattr( self , '_{}'.format( s ) ) )
                for s in Group.SETS
                if getattr( self , '_{}'.format( s ) )
        })
        return rv

    #---------------------------------------------------------------------------

    @property
    def members( self ):
        """
        La liste des membres, triée par ordre alphabétique.
        """
        return sorted( self._members )

    @property
    def members_set( self ):
        """
        L'ensemble des membres, modifiable.
        """
        return self._members

    @property
    def has_members( self ):
        """
        La présence, ou non, de membres dans le groupe
        """
        return bool( self._members )

    @property
    def senders( self ):
        """
        La liste des expéditeurs autorisés, triée par ordre alphabétique.
        """
        return sorted( self._senders )

    @property
    def senders_set( self ):
        """
        L'ensemble des expéditeurs autorisés, modifiable.
        """
        return self._senders

    @property
    def has_senders( self ):
        """
        La présence, ou non, d'expéditeurs autorisés
        """
        return bool( self._senders )

    @property
    def aliases( self ):
        """
        La liste des alias du groupe, triée par ordre alphabétique.
        """
        return sorted( self._aliases )

    @property
    def aliases_set( self ):
        """
        L'ensemble des alias du groupe, modifiable
        """
        return self._aliases

    @property
    def has_aliases( self ):
        """
        La présence, ou non, d'alias pour ce groupe
        """
        return bool( self._aliases )

    #---------------------------------------------------------------------------

    @property
    def description( self ):
        return self._description

    @description.setter
    def description( self , value ):
        if isinstance( value , str ) or value is None:
            self._description = value
        else:
            raise TypeError

    #---------------------------------------------------------------------------

    @property
    def displayName( self ):
        return self._displayName

    @displayName.setter
    def displayName( self , value ):
        if isinstance( value , str ) or value is None:
            self._displayName = value
        else:
            raise TypeError

    #---------------------------------------------------------------------------

    @property
    def zimbraDistributionListSendShareMessageToNewMembers( self ):
        return self._zimbraDistributionListSendShareMessageToNewMembers

    @zimbraDistributionListSendShareMessageToNewMembers.setter
    def zimbraDistributionListSendShareMessageToNewMembers( self , value ):
        v = Group._from_bool( value , 'TRUE' , 'FALSE' , lambda x : x.upper( ) )
        self._zimbraDistributionListSendShareMessageToNewMembers = v

    #---------------------------------------------------------------------------

    @property
    def zimbraHideInGal( self ):
        return self._zimbraHideInGal

    @zimbraHideInGal.setter
    def zimbraHideInGal( self , value ):
        v = Group._from_bool( value , 'TRUE' , 'FALSE' , lambda x : x.upper( ) )
        self._zimbraHideInGal = v

    #---------------------------------------------------------------------------

    @property
    def zimbraMailStatus( self ):
        return self._zimbraMailStatus

    @zimbraMailStatus.setter
    def zimbraMailStatus( self , value ):
        self._zimbraMailStatus = Group._from_bool( value ,
                'enabled' , 'disabled' , lambda x : x.lower( ) )

    #---------------------------------------------------------------------------

    @property
    def zimbraNotes( self ):
        return self._zimbraNotes

    @zimbraNotes.setter
    def zimbraNotes( self , value ):
        if isinstance( value , str ) or value is None:
            self._zimbraNotes = value
        else:
            raise TypeError
