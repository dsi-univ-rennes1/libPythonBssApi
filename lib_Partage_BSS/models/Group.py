# -*-coding:utf-8 -*
import json

from lib_Partage_BSS import utils
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.models.GlobalModel import GlobalModel


class Group( GlobalModel ):

    ATTRIBUTES = (
            'description' , 'displayName' ,
            'zimbraDistributionListSendShareMessageToNewMembers' ,
            'zimbraHideInGal' , 'zimbraMailStatus' , 'zimbraNotes'
        )

    def __init__( self , name = None ):
        if name is not None and not ( isinstance( name , str )
                and utils.checkIsMailAddress( name ) ):
            raise TypeError
        GlobalModel.__init__( self , name )
        for a in Group.ATTRIBUTES:
            setattr( self , '_{}'.format( a ) , None )
        self._members = set( )
        self._senders = set( )
        self._aliases = set( )

    #---------------------------------------------------------------------------

    @staticmethod
    def _get_set( output , data , name , sub = None ):
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
        try:
            group = Group( data[ 'name' ] )
        except TypeError:
            raise NameException( "L'adresse mail {} n'est pas valide".format(
                    data[ 'name' ] ) )
        for a in Group.ATTRIBUTES:
            if a in data:
                setattr( group , a , data[ a ] )
        Group._get_set( group._members , data , 'members' , 'member' )
        Group._get_set( group._aliases , data , 'zimbraMailAlias' )
        return group

    def senders_from_bss( self , data ):
        self._senders.clear( )
        Group._get_set( self._senders , data , 'accounts' , 'account' )
        return self.senders

    #---------------------------------------------------------------------------

    @property
    def members( self ):
        return sorted( self._members )

    @property
    def senders( self ):
        return sorted( self._senders )

    @property
    def aliases( self ):
        return sorted( self._aliases )

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
        return self._zimbraMailStatus == 'enabled'

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
