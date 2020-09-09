# -*-coding:utf-8 -*
import json

from lib_Partage_BSS import utils
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.models.GlobalModel import GlobalModel
from collections import OrderedDict

class Account(GlobalModel):
    """
    Classe représentant un compte dans Partage

    :ivar _id: l'identifiant du compte
    :ivar _admin: le niveau d'administrateur du compte (ADMIN,...)
    :ivar _co: ...
    :ivar _company: ...
    :ivar _description: Description du compte
    :ivar _facsimileTelephoneNumber: Numéro de Fax du compte
    :ivar _homePhone: ...
    :ivar _initials: ...
    :ivar _l: ...
    :ivar _mavTransformation: ...
    :ivar _mavRedirection: ...
    :ivar _mobile: Numéro de mobile associé au compte
    :ivar _pager: ...
    :ivar _postalCode: Code postal associé au compte
    :ivar _used: Espace utilisé par le compte (en octet)
    :ivar _quota: Espace disponible pour le compte (en octet)
    :ivar _carLicense: EduPersonPrincipalName l'identifiant fondation du compte
    :ivar _givenName: Prénom de la personne
    :ivar _displayName: Nom complet de la personne
    :ivar _businessCategory: ...
    :ivar _sn: Nom de la personne
    :ivar _st:
    :ivar _street: Rue de la personne
    :ivar _telephoneNumber: Numéro de téléphone de la personne
    :ivar _title: ...
    :ivar _zimbraAccountStatus: Etat du compte défaut active (active,closed)
    :ivar _zimbraFeatureBriefcasesEnabled: ...
    :ivar _zimbraFeatureCalendarEnabled: ...
    :ivar _zimbraFeatureMailEnabled: ...
    :ivar _zimbraFeatureMailForwardingEnabled: Permettre à l'utilisateur d'indiquer une adresse de redirection (TRUE,FALSE)
    :ivar _zimbraFeatureOptionsEnabled: ...
    :ivar _zimbraFeatureTasksEnabled: ...
    :ivar _zimbraHideInGal: Masquer dans la GAL (TRUE,FALSE)
    :ivar _zimbraLastLogonTimestamp: Timestamp de la dernière connection au compte
    :ivar _zimbraMailQuota: ...
    :ivar _zimbraNotes: ...
    :ivar _zimbraPasswordMustChange: Forcer le changement de mot de passe à la prochaine connection (TRUE,FALSE)
    :ivar _zimbraPrefMailForwardingAddress: Adresse de redirection saisie par l?utilisateur
    :ivar _zimbraPrefMailLocalDeliveryDisabled: Ne pas conserver de copie des mails sur le client local
    :ivar _zimbraMailAlias: Liste des alias du compte
    :ivar _zimbraMailCanonicalAddress: Adresse email visible pour les messages sortants
    :ivar _zimbraPrefFromDisplay: Adresse email visible pour les messages sortants
    :ivar _zimbraCOSId: Id de la classe de Service du compte
    :ivar _zimbraZimletAvailableZimlets: Les zimlets disponible pour le compte
    """
    def __init__(self, name):
        if utils.checkIsMailAddress(name):
            GlobalModel.__init__(self, name)
            self._id = None
            self._admin = None
            self._businessCategory = None
            self._co = None
            self._company = None
            self._description = None
            self._displayName = None
            self._carLicense = None
            self._facsimileTelephoneNumber = None
            self._givenName = None
            self._homePhone = None
            self._initials = None
            self._l = None
            self._mavTransformation = None
            self._mavRedirection = None
            self._mobile = None
            self._pager = None
            self._postalCode = None
            self._quota = None
            self._sn = None
            self._st = None
            self._street = None
            self._telephoneNumber = None
            self._title = None
            self._used = None
            self._zimbraAccountStatus = None
            self._zimbraFeatureBriefcasesEnabled = None
            self._zimbraFeatureCalendarEnabled = None
            self._zimbraFeatureMailEnabled = None
            self._zimbraFeatureMailForwardingEnabled = None
            self._zimbraFeatureOptionsEnabled = None
            self._zimbraFeatureTasksEnabled = None
            self._zimbraHideInGal = None
            self._zimbraLastLogonTimestamp = None
            self._zimbraMailQuota = None
            self._zimbraNotes = None
            self._zimbraPasswordMustChange = None
            self._zimbraPrefMailForwardingAddress = None
            self._zimbraPrefMailLocalDeliveryDisabled = None
            self._zimbraMailAlias = None
            self._zimbraMailCanonicalAddress = None
            self._zimbraPrefFromDisplay = None
            self._zimbraCOSId = None
            self._zimbraZimletAvailableZimlets = None

        else:
            raise NameException("Le nom donné n'est pas une adresse mail")

    @property
    def id(self):
        return self._id

    @property
    def admin(self):
        return self._admin

    @property
    def businessCategory(self):
        return self._businessCategory

    @property
    def co(self):
        return self._co

    @property
    def company(self):
        return self._company

    @property
    def description(self):
        return self._description

    @property
    def displayName(self):
        return self._displayName

    @property
    def carLicense(self):
        return self._carLicense

    @property
    def facsimileTelephoneNumber(self):
        return self._facsimileTelephoneNumber

    @property
    def givenName(self):
        return self._givenName

    @property
    def homePhone(self):
        return self._homePhone

    @property
    def initials(self):
        return self._initials

    @property
    def l(self):
        return self._l

    @property
    def mavTransformation(self):
        return self._mavTransformation

    @property
    def mavRedirection(self):
        return self._mavRedirection

    @property
    def mobile(self):
        return self._mobile

    @property
    def pager(self):
        return self._pager

    @property
    def postalCode(self):
        return self._postalCode

    @property
    def quota(self):
        return self._quota

    @property
    def sn(self):
        return self._sn

    @property
    def st(self):
        return self._st

    @property
    def street(self):
        return self._street

    @property
    def telephoneNumber(self):
        return self._telephoneNumber

    @property
    def title(self):
        return self._title

    @property
    def used(self):
        return self._used

    @property
    def zimbraAccountStatus(self):
        return self._zimbraAccountStatus

    @property
    def zimbraFeatureBriefcasesEnabled(self):
        return self._zimbraFeatureBriefcasesEnabled

    @property
    def zimbraFeatureCalendarEnabled(self):
        return self._zimbraFeatureCalendarEnabled

    @property
    def zimbraFeatureMailEnabled(self):
        return self._zimbraFeatureMailEnabled

    @property
    def zimbraFeatureMailForwardingEnabled(self):
        return self._zimbraFeatureMailForwardingEnabled

    @property
    def zimbraFeatureOptionsEnabled(self):
        return self._zimbraFeatureOptionsEnabled

    @property
    def zimbraFeatureTasksEnabled(self):
        return self._zimbraFeatureTasksEnabled

    @property
    def zimbraHideInGal(self):
        return self._zimbraHideInGal

    @property
    def zimbraLastLogonTimestamp(self):
        return self._zimbraLastLogonTimestamp

    @property
    def zimbraMailAlias(self):
        return self._zimbraMailAlias

    @property
    def zimbraMailQuota(self):
        return self._zimbraMailQuota

    @property
    def zimbraMailCanonicalAddress(self):
        return self._zimbraMailCanonicalAddress

    @property
    def zimbraNotes(self):
        return self._zimbraNotes

    @property
    def zimbraPasswordMustChange(self):
        return self._zimbraPasswordMustChange

    @property
    def zimbraPrefFromDisplay(self):
        return self._zimbraPrefFromDisplay

    @property
    def zimbraPrefMailForwardingAddress(self):
        return self._zimbraPrefMailForwardingAddress

    @property
    def zimbraPrefMailLocalDeliveryDisabled(self):
        return self._zimbraPrefMailLocalDeliveryDisabled

    @property
    def zimbraCOSId(self):
        return self._zimbraCOSId

    @property
    def zimbraZimletAvailableZimlets(self):
        return self._zimbraZimletAvailableZimlets

    @admin.setter
    def admin(self, value):
        if isinstance(value, str) or value is None:
            self._admin = value
        else:
            raise TypeError

    @businessCategory.setter
    def businessCategory(self, value):
        if isinstance(value, str) or value is None:
            self._businessCategory = value
        else:
            raise TypeError

    @co.setter
    def co(self, value):
        if isinstance(value, str) or value is None:
            self._co = value
        else:
            raise TypeError

    @company.setter
    def company(self, value):
        if isinstance(value, str) or value is None:
            self._company = value
        else:
            raise TypeError

    @description.setter
    def description(self, value):
        if isinstance(value, str) or value is None:
            self._description = value
        else:
            raise TypeError

    @displayName.setter
    def displayName(self, value):
        if isinstance(value, str) or value is None:
            self._displayName = value
        else:
            raise TypeError

    @carLicense.setter
    def carLicense(self, value):
        if isinstance(value, str) or value is None:
            self._carLicense = value
        else:
            raise TypeError

    @facsimileTelephoneNumber.setter
    def facsimileTelephoneNumber(self, value):
        if isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                self._facsimileTelephoneNumber = value
        else:
            raise TypeError

    @givenName.setter
    def givenName(self, value):
        if isinstance(value, str) or value is None:
            self._givenName = value
        else:
            raise TypeError

    @homePhone.setter
    def homePhone(self, value):
        if isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                self._homePhone = value
        else:
            raise TypeError

    @initials.setter
    def initials(self, value):
        if isinstance(value, str) or value is None:
            self._initials = value
        else:
            raise TypeError

    @l.setter
    def l(self, value):
        if isinstance(value, str) or value is None:
            self._l = value
        else:
            raise TypeError

    @mavTransformation.setter
    def mavTransformation(self, value):
        if value is None:
            self._mavTransformation = None
        elif utils.checkBoolean( value ):
            self._mavTransformation = utils.convertToBoolean( value )
        else:
            raise TypeError

    @mavRedirection.setter
    def mavRedirection(self, value):

        if isinstance(value, str) or value is None:
            self._mavRedirection = value
        else:
            raise TypeError

    @mobile.setter
    def mobile(self, value):
        if isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                self._mobile = value
        else:
            raise TypeError

    @pager.setter
    def pager(self, value):
        if isinstance(value, str) or value is None:
            self._pager = value
        else:
            raise TypeError

    @postalCode.setter
    def postalCode(self, value):
        if isinstance(value, int):
            self._postalCode = str(value)
        elif isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                self._postalCode = value
        else:
            raise TypeError

    @quota.setter
    def quota(self, value):
        if isinstance(value, int) or value is None:
            self._quota = value
        elif isinstance(value , str):
            try:
                self._quota = int(value)
            except ValueError:
                raise TypeError
        else:
            raise TypeError

    @sn.setter
    def sn(self, value):
        if isinstance(value, str) or value is None:
            self._sn = value
        else:
            raise TypeError

    @st.setter
    def st(self, value):
        if isinstance(value, str) or value is None:
            self._st = value
        else:
            raise TypeError

    @street.setter
    def street(self, value):
        if isinstance(value, str) or value is None:
            self._street = value
        else:
            raise TypeError

    @telephoneNumber.setter
    def telephoneNumber(self, value):
        if isinstance(value, str) or value is None:
            if utils.checkIsNum(value):
                self._telephoneNumber = value
        else:
            raise TypeError

    @title.setter
    def title(self, value):
        if isinstance(value, str) or value is None:
            self._title = value
        else:
            raise TypeError

    @used.setter
    def used(self, value):
        if isinstance(value, int) or value is None:
            self._used = value
        elif isinstance( value , str ):
            try:
                self._used = int( value )
            except ValueError:
                raise TypeError
        else:
            raise TypeError

    @zimbraAccountStatus.setter
    def zimbraAccountStatus(self, value):
        if value == "active" or value == "closed" or value == "locked":
            self._zimbraAccountStatus = value
        else:
            raise TypeError

    @zimbraFeatureBriefcasesEnabled.setter
    def zimbraFeatureBriefcasesEnabled(self, value):
        if value is None:
            self._zimbraFeatureBriefcasesEnabled = None
        elif utils.checkBoolean( value ):
            self._zimbraFeatureBriefcasesEnabled = utils.convertToBoolean(
                    value )
        else:
            raise TypeError

    @zimbraFeatureCalendarEnabled.setter
    def zimbraFeatureCalendarEnabled(self, value):
        if value is None:
            self._zimbraFeatureCalendarEnabled = None
        elif utils.checkBoolean( value ):
            self._zimbraFeatureCalendarEnabled = utils.convertToBoolean( value )
        else:
            raise TypeError

    @zimbraFeatureMailEnabled.setter
    def zimbraFeatureMailEnabled(self, value):
        if value is None:
            self._zimbraFeatureMailEnabled = None
        elif utils.checkBoolean( value ):
            self._zimbraFeatureMailEnabled = utils.convertToBoolean( value )
        else:
            raise TypeError

    @zimbraFeatureMailForwardingEnabled.setter
    def zimbraFeatureMailForwardingEnabled(self, value):
        if value is None:
            self._zimbraFeatureMailForwardingEnabled = None
        elif utils.checkBoolean( value ):
            self._zimbraFeatureMailForwardingEnabled = utils.convertToBoolean(
                    value )
        else:
            raise TypeError

    @zimbraFeatureOptionsEnabled.setter
    def zimbraFeatureOptionsEnabled(self, value):
        if value is None:
            self._zimbraFeatureOptionsEnabled = None
        elif utils.checkBoolean( value ):
            self._zimbraFeatureOptionsEnabled = utils.convertToBoolean( value )
        else:
            raise TypeError

    @zimbraFeatureTasksEnabled.setter
    def zimbraFeatureTasksEnabled(self, value):
        if value is None:
            self._zimbraFeatureTasksEnabled = None
        elif utils.checkBoolean( value ):
            self._zimbraFeatureTasksEnabled = utils.convertToBoolean( value )
        else:
            raise TypeError

    @zimbraHideInGal.setter
    def zimbraHideInGal(self, value):
        if value is None:
            self._zimbraHideInGal = None
        elif utils.checkBoolean( value ):
            self._zimbraHideInGal = utils.convertToBoolean( value )
        else:
            raise TypeError

    @zimbraMailQuota.setter
    def zimbraMailQuota(self, value):
        if isinstance(value, int) or value is None:
            self._zimbraMailQuota = value
        elif isinstance(value, str):
            try:
                self._zimbraMailQuota = int( value )
            except ValueError:
                raise TypeError
        else:
            raise TypeError

    @zimbraMailAlias.setter
    def zimbraMailAlias(self, value):
        if isinstance(value, list) or value is None:
            self._zimbraMailAlias = value
        else:
            raise TypeError

    @zimbraMailCanonicalAddress.setter
    def zimbraMailCanonicalAddress(self, value):
        if isinstance(value, str) or value is None:
            if utils.checkIsMailAddress(value):
                self._zimbraMailCanonicalAddress = value
            else:
                raise NameException("L'adresse mail " + value + " n'est pas une adresse mail valide")
        else:
            raise TypeError

    @zimbraLastLogonTimestamp.setter
    def zimbraLastLogonTimestamp(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraLastLogonTimestamp = value
        else:
            raise TypeError

    @zimbraNotes.setter
    def zimbraNotes(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraNotes = value
        else:
            raise TypeError

    @zimbraPasswordMustChange.setter
    def zimbraPasswordMustChange(self, value):
        if value is None:
            self._zimbraPasswordMustChange = None
        elif utils.checkBoolean( value ):
            self._zimbraPasswordMustChange = utils.convertToBoolean( value )
        else:
            raise TypeError

    @zimbraPrefFromDisplay.setter
    def zimbraPrefFromDisplay(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraPrefFromDisplay = value
        else:
            raise TypeError

    @zimbraPrefMailForwardingAddress.setter
    def zimbraPrefMailForwardingAddress(self, value):
        if isinstance(value, str) or value is None:
            if utils.checkIsMailAddress(value):
                self._zimbraPrefMailForwardingAddress = value
            else:
                raise NameException("L'adresse mail " + value + " n'est pas une adresse mail valide")
        else:
            raise TypeError

    @zimbraPrefMailLocalDeliveryDisabled.setter
    def zimbraPrefMailLocalDeliveryDisabled(self, value):
        if value is None:
            self._zimbraPrefMailLocalDeliveryDisabled = None
        elif utils.checkBoolean( value ):
            self._zimbraPrefMailLocalDeliveryDisabled = utils.convertToBoolean(
                    value )
        else:
            raise TypeError

    @zimbraCOSId.setter
    def zimbraCOSId(self, value):
        if isinstance(value, str) or value is None:
            self._zimbraCOSId = value
        else:
            raise TypeError

    def addZimbraZimletAvailableZimlets(self, value):
        if isinstance(value, str):
            if self._zimbraZimletAvailableZimlets is None:
                self._zimbraZimletAvailableZimlets = []
            if value not in self._zimbraZimletAvailableZimlets:
                self._zimbraZimletAvailableZimlets.append(value)
        else:
            raise TypeError

    def removeZimbraZimletAvailableZimlets(self, valueToRemove):
        if isinstance(valueToRemove, str):
            if valueToRemove in self._zimbraZimletAvailableZimlets:
                self._zimbraZimletAvailableZimlets.remove(valueToRemove)
        else:
            raise TypeError

    def resetZimbraZimletAvailableZimlets(self):
        self._zimbraZimletAvailableZimlets = 'DELETE_ARRAY'

    def fillAccount(self, listOfAttr, allowNameChange=False):
        if not isinstance(listOfAttr, dict) and not isinstance(listOfAttr, list):
            raise TypeError
        for attr in listOfAttr:
            if attr == "name" and not allowNameChange:
                continue
            propattr = getattr(self.__class__, attr, None)
            if isinstance(propattr, property) and propattr.fset is not None:
                if listOfAttr[attr] == "None":
                    propattr.fset(self, None)
                else:
                    propattr.fset(self, listOfAttr[attr])

    def toData(self, checkName = True):
        """
        Transforme les données du compte en un dictionnaire pouvant être
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

            if isinstance(attrValue, list) or attrValue == 'DELETE_ARRAY':
                # On prévoit une valeur spéciale 'DELETE_ARRAY' pour effacer un attribut de type tableau
                if attrValue == 'DELETE_ARRAY':
                    attrValue = ''

                attrKey = attrKey+'[]'

            if isinstance(attrValue, bool):
                attrValue = utils.changeBooleanToString(attrValue)

            data[attrKey] = attrValue
        return data


def importJsonAccount(jsonAccount):
    json_data = open(jsonAccount)
    data = json.load(json_data)

    if "name" not in data:
        raise NameException("Adresse mail non présent dans le fichier json")
    account = Account(data["name"])
    for attr in data:
        if attr == "name":
            continue
        propattr = getattr(account.__class__, attr, None)
        if isinstance(propattr, property):
                #and propattr.fset is not None:
            if data[attr] == "None":
                delattr(account,attr)
                #propattr.fset(account, None)
            else:
                propattr.fset(account, data[attr])
    return account
