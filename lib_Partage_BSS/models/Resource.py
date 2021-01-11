# -*-coding:utf-8 -*
import array
import collections
import json

from lib_Partage_BSS import utils
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.models.GlobalModel import GlobalModel


class Resource( GlobalModel ):
    """
    Classe représentant une ressource dans Partage.

    :ivar _description: description du de la ressource
    :ivar _displayName: nom d'affichage de la ressouce
    :ivar _co: non du pays de la ressouce
    :ivar _l: nom de la ville de la ressouce
    :ivar _postalCode: code postal de la ressouce
    :ivar _st: etat de la ressource
    :ivar _street: rue de la ressource
    :ivar _userPassword: Empreinte du mot de passe de la ressource
    :ivar _zimbraAccountStatus: etat de la ressource (par defaut active)
    :ivar _zimbraCalResAutoAcceptDecline: accepte ou decline automatiquement les invitations
    :ivar _zimbraCalResAutoDeclineIfBusy: decline automatiquement les invitations /
                                        si risque de conflit
    :ivar _zimbraCalResAutoDeclineRecurring: decline automatiquement les invitations recurrentes
    :ivar _zimbraCalResBuilding: batiment de la ressource
    :ivar _zimbraCalResCapacity: Capacité de la ressource
    :ivar _zimbraCalResContactEmail: adresse mail du contact de la ressource
    :ivar _zimbraCalResContactName: nom du contact de la ressource
    :ivar _zimbraCalResContactPhone: telephone du contact de la ressource
    :ivar _zimbraCalResFloor: etage de la ressource
    :ivar _zimbraCalResLocationDisplayName: nom du lieu affiché
    :ivar _zimbraCalResRoom: salle de la ressource
    :ivar _zimbraCalResSite: lieu de la ressource
    :ivar _zimbraCalResType: type de ressource
    :ivar _zimbraNotes: note libre
    :ivar _zimbraPrefCalendarForwardInvitesTo: type de faire suivre les invitations de /
                                calandrier a cette adresse

    """

    # Attributs utilisés dans {Create,Modify}Account
    ATTRIBUTES = (
            'description' , 'displayName' , 'co', 'l', 'postalCode', 'street',
            'zimbraAccountStatus', 'zimbraCalResLocationDisplayName', 'st' ,
            'zimbraCalResSite' , 'zimbraCalResBuilding' , 'zimbraCalResFloor' ,
            'zimbraCalResRoom' , 'zimbraCalResCapacity' , 'zimbraCalResAutoAcceptDecline' ,
            'zimbraCalResAutoDeclineIfBusy' , 'zimbraCalResAutoDeclineRecurring' ,
            'zimbraCalResContactEmail' , 'zimbraCalResContactName' , 'zimbraNotes' ,
            'zimbraPrefCalendarForwardInvitesTo'
        )

    def __init__( self , name = None ):
        if name is not None and not isinstance( name , str ):
            raise TypeError
        if name is not None and not utils.checkIsMailAddress( name ):
            raise NameException( "Adresse mail {} invalide".format( name ) )

        GlobalModel.__init__( self , name )

        for a in Resource.ATTRIBUTES:
            setattr( self , '_{}'.format( a ) , None )

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
        Partage, soit via GetResource soit via GetAllResources. Dans le premier cas,
        tous les champs à l'exception de la liste des utilisateurs autorisés à
        expédier avec l'adresse de la resource seront mis à jour.

        :param data: les données de la resource reçues depuis le serveur Partage

        :raises TypeError: un champ n'a pas le format attendu

        :return: l'instance de la Resource créée, avec ses champs renseignés
        """
        ressource = Resource( data[ 'name' ] )
        ressource.from_dict( data )
        return ressource

    def from_dict( self , data , allow_name_resType = True ):
        """
        Met à jour les champs d'une instance à partir d'un dictionnaire. Seuls
        les attributs, et optionellement le nom et zimbraCalResType, peuvent être modifiés par cette
        méthode.

        :param data: le dictionnaire à partir duquel on veut mettre à jour les \
                données
        :param allow_name_resType: permettre la modification du champ 'name' à partir \
                du dictionnaire; si False, les entrées 'name' et 'zimbraCalResType' dans le \
                dictionnaire sera ignorée

        :raises TypeError: un champ n'a pas le format attendu
        """
        attrs = (
                ( 'name', 'zimbraCalResType' , *Resource.ATTRIBUTES ) if allow_name_resType
                else Resource.ATTRIBUTES
            )
        for a in attrs:
            if a in data:
                if a == "zimbraPrefCalendarForwardInvitesTo":
                    self.addZimbraPrefCalendarForwardInvitesTo(data[a])
                else:
                    setattr( self , a , data[ a ] )

    def to_bss( self ):
        """
        Génère un dictionnaire pouvant être utilisé pour créer ou modifier une
        resource sur le serveur.

        :return: le dictionnaire contenant les attributs
        """
        rv = { }
        for a in ( 'name', 'zimbraCalResType', 'zimbraPrefCalendarForwardInvitesTo', *Resource.ATTRIBUTES ):
            value = getattr( self , a )
            if value is not None:
                rv[ a ] = value
        return rv

    def toData(self, checkName = True):
        """
        Transforme les données d'une resource en un dictionnaire pouvant être
        utilisé avec l'API BSS, après avoir éventuellement vérifié
        l'adresse.

        :param bool checkName: vérifie l'adresse associée au compte

        :raises NameException: exception levée si le nom n'est pas une \
        adresse mail valide

        :return: le dictionnaire contenant les informations au sujet du \
        compte et pouvant être passé à l'API BSS.
        """
        if self.name is None:
            raise NameException( 'Aucune adresse mail spécifiée.' )
        if checkName and not utils.checkIsMailAddress( self.name ):
            raise NameException("L'adresse mail " + self.name
                    + " n'est pas valide")
        data = {}
        for attr in self.__dict__:
            attrValue = self.__getattribute__(attr)

            # On ne prend pas le préfixe '_'
            attrKey = attr[1:]

            if (self.__getattribute__(attr) is None ):
                continue

            if isinstance(attrValue, list):
                attrKey = attrKey+'[]'

            if isinstance(attrValue, bool):
                attrValue = utils.changeBooleanToString(attrValue)

            data[attrKey] = attrValue
        return data

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
        return Resource.from_json_record( data )

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
        resource = Resource( record[ 'name' ] if 'name' in record else None )
        for a in Resource.ATTRIBUTES:
            if a in record:
                setattr( resource , a , record[ a ] )
        return resource

    def addZimbraPrefCalendarForwardInvitesTo(self, value):
        if isinstance(value, str) or value is None:
            if self._zimbraPrefCalendarForwardInvitesTo is None:
                self._zimbraPrefCalendarForwardInvitesTo = []
            if value not in self._zimbraPrefCalendarForwardInvitesTo:
                if utils.checkIsMailAddress(value):
                    self._zimbraPrefCalendarForwardInvitesTo.append(value)
                else:
                    raise TypeError("addZimbraPrefCalendarForwardInvitesTo")
        elif isinstance(value, collections.OrderedDict):
            if isinstance(value['zimbraPrefCalendarForwardInvitesTo'], list):
                if self._zimbraPrefCalendarForwardInvitesTo is None:
                    self._zimbraPrefCalendarForwardInvitesTo = []
                if value['zimbraPrefCalendarForwardInvitesTo'] not in self._zimbraPrefCalendarForwardInvitesTo:
                    self._zimbraPrefCalendarForwardInvitesTo += value['zimbraPrefCalendarForwardInvitesTo']
        else:
            raise TypeError("addZimbraPrefCalendarForwardInvitesTo")

    def removeZimbraPrefCalendarForwardInvitesTo(self, valueToRemove):
        if isinstance(valueToRemove, str):
            if valueToRemove in self._zimbraPrefCalendarForwardInvitesTo:
                self._zimbraPrefCalendarForwardInvitesTo.remove(valueToRemove)
        else:
            raise TypeError("removeZimbraPrefCalendarForwardInvitesTo")


    """
    def removeZimbraPrefCalendarForwardInvitesTo(self, valueToRemove):
        if isinstance(valueToRemove, str):
            if valueToRemove in self._zimbraPrefCalendarForwardInvitesTo:
                if isinstance(self._zimbraPrefCalendarForwardInvitesTo, list):
                    print("LIST")
                    if len(self._zimbraPrefCalendarForwardInvitesTo) == 1:
                        self._zimbraPrefCalendarForwardInvitesTo.clear()
                    else:
                        self._zimbraPrefCalendarForwardInvitesTo.remove(valueToRemove)
                elif isinstance(self._zimbraPrefCalendarForwardInvitesTo, str):
                    print("STR")
                    print(self._zimbraPrefCalendarForwardInvitesTo)
                    print(valueToRemove)
                    self._zimbraPrefCalendarForwardInvitesTo=""
                    print(self._zimbraPrefCalendarForwardInvitesTo)
                    print(valueToRemove)
            if len(self._zimbraPrefCalendarForwardInvitesTo) == 0:
                print("LEN = 0")
                self._zimbraPrefCalendarForwardInvitesTo = ""
        else:
            raise TypeError("removeZimbraPrefCalendarForwardInvitesTo")

    """
    # ---------------------------------------------------------------------------

    @property
    def description( self ):
        return self._description

    @description.setter
    def description( self , value ):
        if isinstance( value , str ) or value is None:
            self._description = value
        else:
            raise TypeError("description")

    #---------------------------------------------------------------------------

    @property
    def displayName( self ):
        return self._displayName

    @displayName.setter
    def displayName( self , value ):
        if isinstance( value , str ) or value is None:
            self._displayName = value
        else:
            raise TypeError("displayName")

    #---------------------------------------------------------------------------

    @property
    def co(self):
        return self._co

    @co.setter
    def co(self, value):
        if isinstance(value, str) or value is None:
            self._co = value
        else:
            raise TypeError("co")

    # ---------------------------------------------------------------------------

    @property
    def l(self):
        return self._l

    @l.setter
    def l(self, value):
        if isinstance(value, str) or value is None:
            self._l = value
        else:
            raise TypeError("l")

    # ---------------------------------------------------------------------------

    @property
    def postalCode(self):
        return self._postalCode

    @postalCode.setter
    def postalCode(self, value):
        val = None
        if isinstance(value, collections.OrderedDict):
            if utils.checkIsNum(value['content']):
                val = value['content']
        elif isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                val = value
        else:
            raise TypeError("postalCode")
        self._postalCode = val


    # ---------------------------------------------------------------------------

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, value):
        if isinstance(value, str) or value is None:
            self._street = value
        else:
            raise TypeError("street")

    # ---------------------------------------------------------------------------

    @property
    def st(self):
        return self._st

    @st.setter
    def st(self, value):
        if isinstance(value, str) or value is None:
            self._st = value
        else:
            raise TypeError("st")

    # ---------------------------------------------------------------------------

    @property
    def zimbraAccountStatus( self ):
        return self._zimbraAccountStatus

    @zimbraAccountStatus.setter
    def zimbraAccountStatus( self , value ):
        v = Resource._from_bool( value , 'active' , 'closed' , lambda x : x.lower( ) )
        self._zimbraAccountStatus = v

    #---------------------------------------------------------------------------

    @property
    def zimbraCalResLocationDisplayName(self):
        return self._zimbraCalResLocationDisplayName

    @zimbraCalResLocationDisplayName.setter
    def zimbraCalResLocationDisplayName(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraCalResLocationDisplayName = value
        else:
            raise TypeError("zimbraCalResLocationDisplayName")

    # ---------------------------------------------------------------------------

    @property
    def zimbraCalResSite(self):
        return self._zimbraCalResSite

    @zimbraCalResSite.setter
    def zimbraCalResSite(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraCalResSite = value
        else:
            raise TypeError("zimbraCalResSite")

    # ---------------------------------------------------------------------------

    @property
    def zimbraCalResBuilding(self):
        return self._zimbraCalResBuilding

    @zimbraCalResBuilding.setter
    def zimbraCalResBuilding(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraCalResBuilding = value
        else:
            raise TypeError("zimbraCalResBuilding")

    # ---------------------------------------------------------------------------

    @property
    def zimbraCalResFloor(self):
        return self._zimbraCalResFloor

    @zimbraCalResFloor.setter
    def zimbraCalResFloor(self, value):
        val = None
        if isinstance(value, collections.OrderedDict):
            if utils.checkIsNum(value['content']):
                val = value['content']
        elif isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                val = value
        else:
            raise TypeError("zimbraCalResFloor")
        self._zimbraCalResFloor = val

    # ---------------------------------------------------------------------------

    @property
    def zimbraCalResRoom(self):
        return self._zimbraCalResRoom

    @zimbraCalResRoom.setter
    def zimbraCalResRoom(self, value):
        val = None
        if isinstance(value, collections.OrderedDict):
            if utils.checkIsNum(value['content']):
                val = value['content']
        elif isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                val = value
        else:
            raise TypeError("zimbraCalResRoom")
        self._zimbraCalResRoom = val

    # ---------------------------------------------------------------------------

    @property
    def zimbraCalResCapacity(self):
        return self._zimbraCalResCapacity

    @zimbraCalResCapacity.setter
    def zimbraCalResCapacity(self, value):
        val = None
        if isinstance(value, collections.OrderedDict):
            if utils.checkIsNum(value['content']):
                val = value['content']
        elif isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                val = value
        else:
            raise TypeError("zimbraCalResCapacity")
        self._zimbraCalResCapacity = val

    # ---------------------------------------------------------------------------

    @property
    def zimbraCalResAutoAcceptDecline( self ):
        return self._zimbraCalResAutoAcceptDecline

    @zimbraCalResAutoAcceptDecline.setter
    def zimbraCalResAutoAcceptDecline( self , value ):
        v = Resource._from_bool( value , 'TRUE' , 'FALSE' , lambda x : x.upper( ) )
        self._zimbraCalResAutoAcceptDecline = v

    #---------------------------------------------------------------------------

    @property
    def zimbraCalResAutoDeclineIfBusy(self):
        return self._zimbraCalResAutoDeclineIfBusy

    @zimbraCalResAutoDeclineIfBusy.setter
    def zimbraCalResAutoDeclineIfBusy(self, value):
        v = Resource._from_bool(value, 'TRUE', 'FALSE', lambda x: x.upper())
        self._zimbraCalResAutoDeclineIfBusy = v

    # ---------------------------------------------------------------------------

    @property
    def zimbraCalResAutoDeclineRecurring(self):
        return self._zimbraCalResAutoDeclineRecurring

    @zimbraCalResAutoDeclineRecurring.setter
    def zimbraCalResAutoDeclineRecurring(self, value):
        v = Resource._from_bool(value, 'TRUE', 'FALSE', lambda x: x.upper())
        self._zimbraCalResAutoDeclineRecurring = v

    # ---------------------------------------------------------------------------


    @property
    def zimbraCalResContactEmail( self ):
        return self._zimbraCalResContactEmail

    @zimbraCalResContactEmail.setter
    def zimbraCalResContactEmail( self , value ):
        if isinstance(value, str) or value is None:
            if utils.checkIsMailAddress(value):
                self._zimbraCalResContactEmail = value
            else:
                raise NameException("L'adresse mail " + value + " n'est pas une adresse mail valide")
        else:
            raise TypeError("zimbraCalResContactEmail")

    #---------------------------------------------------------------------------

    @property
    def zimbraCalResContactName(self):
        return self._zimbraCalResContactName

    @zimbraCalResContactName.setter
    def zimbraCalResContactName(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraCalResContactName = value
        else:
            raise TypeError("zimbraCalResContactName")

    # ---------------------------------------------------------------------------

    @property
    def zimbraNotes( self ):
        return self._zimbraNotes

    @zimbraNotes.setter
    def zimbraNotes( self , value ):
        if isinstance( value , str ) or value is None:
            self._zimbraNotes = value
        else:
            raise TypeError("zimbraNotes")

    # ---------------------------------------------------------------------------

    @property
    def zimbraPrefCalendarForwardInvitesTo(self):
        return self._zimbraPrefCalendarForwardInvitesTo