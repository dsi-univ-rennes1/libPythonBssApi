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

    SETS = ( 'members' , 'senders' , 'aliases' )


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
        group.from_dict( data )
        Group._get_set( group._members , data , 'members' , 'member' )
        Group._get_set( group._aliases , data , 'zimbraMailAlias' )
        return group

    def from_dict( self , data , allow_name = False ):
        attrs = (
                ( 'name' , *Group.ATTRIBUTES ) if allow_name
                else Group.ATTRIBUTES
            )
        for a in attrs:
            if a in data:
                setattr( self , a , data[ a ] )

    def senders_from_bss( self , data ):
        self._senders.clear( )
        Group._get_set( self._senders , data , 'accounts' , 'account' )
        return self.senders

    def to_bss( self ):
        rv = { }
        for a in ( 'name' , *Group.ATTRIBUTES ):
            value = getattr( self , a )
            if value is not None:
                rv[ a ] = value
        return rv

    #---------------------------------------------------------------------------

    @staticmethod
    def from_json( source , is_file = False ):
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
        group = Group( record[ 'name' ] if 'name' in record else None )
        for a in Group.ATTRIBUTES:
            if a in record:
                setattr( group , a , record[ a ] )
        for s in Group.SETS:
            if s in record:
                getattr( group , '_{}'.format( s ) ).update( record[ s ] )
        return group

    def to_json_record( self ):
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
        return sorted( self._members )

    @property
    def members_set( self ):
        return self._members

    @property
    def has_members( self ):
        return bool( self._members )

    @property
    def senders( self ):
        return sorted( self._senders )

    @property
    def senders_set( self ):
        return self._senders

    @property
    def has_senders( self ):
        return bool( self._senders )

    @property
    def aliases( self ):
        return sorted( self._aliases )

    @property
    def aliases_set( self ):
        return self._aliases

    @property
    def has_aliases( self ):
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
