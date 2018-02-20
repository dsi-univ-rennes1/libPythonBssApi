# -*-coding:Latin-1 -*
from collections import OrderedDict

from lib_Partage_BSS import utils
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.models.GlobalModel import GlobalModel


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
    :ivar _givenName: Prénom de famille de la personne
    :ivar _displayName: Prénom Nom de la personne
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
    :ivar _zimbraFeatureMailForwardingEnabled: Permettre à l?utilisateur d?indiquer une adresse de redirection (TRUE,FALSE)
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
    def getId(self):
        return self._id

    @property
    def getAdmin(self):
        return self._admin

    @property
    def getBusinessCategory(self):
        return self._businessCategory

    @property
    def getCo(self):
        return self._co

    @property
    def getCompany(self):
        return self._company

    @property
    def getDescription(self):
        return self._description

    @property
    def getDisplayName(self):
        return self._displayName

    @property
    def getCarLicense(self):
        return self._carLicense

    @property
    def getFacsimileTelephoneNumber(self):
        return self._facsimileTelephoneNumber

    @property
    def getGivenName(self):
        return self._givenName

    @property
    def getHomePhone(self):
        return self._homePhone

    @property
    def getInitials(self):
        return self._initials

    @property
    def getL(self):
        return self._l

    @property
    def getMavTransformation(self):
        return self._mavTransformation

    @property
    def getMavRedirection(self):
        return self._mavRedirection

    @property
    def getMobile(self):
        return self._mobile

    @property
    def getPager(self):
        return self._pager

    @property
    def getPostalCode(self):
        return self._postalCode

    @property
    def getQuota(self):
        return self._quota

    @property
    def getSn(self):
        return self._sn

    @property
    def getSt(self):
        return self._st

    @property
    def getStreet(self):
        return self._street

    @property
    def getTelephoneNumber(self):
        return self._telephoneNumber

    @property
    def getTitle(self):
        return self._title

    @property
    def getUsed(self):
        return self._used

    @property
    def getZimbraAccountStatus(self):
        return self._zimbraAccountStatus

    @property
    def getZimbraFeatureBriefcasesEnabled(self):
        return self._zimbraFeatureBriefcasesEnabled

    @property
    def getZimbraFeatureCalendarEnabled(self):
        return self._zimbraFeatureCalendarEnabled

    @property
    def getZimbraFeatureMailEnabled(self):
        return self._zimbraFeatureMailEnabled

    @property
    def getZimbraFeatureMailForwardingEnabled(self):
        return self._zimbraFeatureMailForwardingEnabled

    @property
    def getZimbraFeatureOptionsEnabled(self):
        return self._zimbraFeatureOptionsEnabled

    @property
    def getZimbraFeatureTasksEnabled(self):
        return self._zimbraFeatureTasksEnabled

    @property
    def getZimbraHideInGal(self):
        return self._zimbraHideInGal

    @property
    def getZimbraLastLogonTimestamp(self):
        return self._zimbraLastLogonTimestamp

    @property
    def getZimbraMailAlias(self):
        return self._zimbraMailAlias

    @property
    def getZimbraMailQuota(self):
        return self._zimbraMailQuota

    @property
    def getZimbraMailCanonicalAddress(self):
        return self._zimbraMailCanonicalAddress

    @property
    def getZimbraNotes(self):
        return self._zimbraNotes

    @property
    def getZimbraPasswordMustChange(self):
        return self._zimbraPasswordMustChange

    @property
    def getZimbraPrefFromDisplay(self):
        return self._zimbraPrefFromDisplay

    @property
    def getZimbraPrefMailForwardingAddress(self):
        return self._zimbraPrefMailForwardingAddress

    @property
    def getZimbraPrefMailLocalDeliveryDisabled(self):
        return self._zimbraPrefMailLocalDeliveryDisabled

    @property
    def getZimbraCOSId(self):
        return self._zimbraCOSId

    @property
    def getZimbraZimletAvailableZimlets(self):
        return self._zimbraZimletAvailableZimlets

    def setId(self, newValue):
        if isinstance(newValue, str):
            self._id = newValue
        else:
            raise TypeError

    def setAdmin(self, newValue):
        if isinstance(newValue, str):
            self._admin = newValue
        else:
            raise TypeError

    def setBusinessCategory(self, newValue):
        if isinstance(newValue, str):
            self._businessCategory = newValue
        else:
            raise TypeError

    def setCo(self, newValue):
        if isinstance(newValue, str):
            self._co = newValue
        else:
            raise TypeError

    def setCompany(self, newValue):
        if isinstance(newValue, str):
            self._company = newValue
        else:
            raise TypeError

    def setDescription(self, newValue):
        if isinstance(newValue, str):
            self._description = newValue
        else:
            raise TypeError

    def setDisplayName(self, newValue):
        if isinstance(newValue, str):
            self._displayName = newValue
        else:
            raise TypeError

    def setCarLicense(self, newValue):
        if isinstance(newValue, str):
            self._carLicense = newValue
        else:
            raise TypeError

    def setFacsimileTelephoneNumber(self, newValue):
        if isinstance(newValue, str):
            if utils.checkIsNum(newValue):
                self._facsimileTelephoneNumber = newValue
        else:
            raise TypeError

    def setGivenName(self, newValue):
        if isinstance(newValue, str):
            self._givenName = newValue
        else:
            raise TypeError

    def setHomePhone(self, newValue):
        if isinstance(newValue, str):
            if utils.checkIsNum(newValue):
                self._homePhone = newValue
        else:
            raise TypeError

    def setInitials(self, newValue):
        if isinstance(newValue, str):
            self._initials = newValue
        else:
            raise TypeError

    def setL(self, newValue):
        if isinstance(newValue, str):
            self._l = newValue
        else:
            raise TypeError

    def setMavTransformation(self, newValue):
        if isinstance(newValue, bool):
            self._mavTransformation = newValue
        else:
            raise TypeError

    def setMavRedirection(self, newValue):

        if isinstance(newValue, str) or newValue is None:
            self._mavRedirection = newValue
        else:
            raise TypeError

    def setMobile(self, newValue):
        if isinstance(newValue, str):
            if utils.checkIsNum(newValue):
                self._mobile = newValue
        else:
            raise TypeError

    def setPager(self, newValue):
        if isinstance(newValue, str):
            self._pager = newValue
        else:
            raise TypeError

    def setPostalCode(self, newValue):
        if isinstance(newValue, str):
            if utils.checkIsNum(newValue):
                self._postalCode = newValue
        else:
            raise TypeError

    def setQuota(self, newValue):
        if isinstance(newValue, int):
            self._quota = newValue
        else:
            raise TypeError

    def setSn(self, newValue):
        if isinstance(newValue, str):
            self._sn = newValue
        else:
            raise TypeError

    def setSt(self, newValue):
        if isinstance(newValue, str):
            self._st = newValue
        else:
            raise TypeError

    def setStreet(self, newValue):
        if isinstance(newValue, str):
            self._street = newValue
        else:
            raise TypeError

    def setTelephoneNumber(self, newValue):
        if isinstance(newValue, str):
            if utils.checkIsNum(newValue):
                self._telephoneNumber = newValue
        else:
            raise TypeError

    def setTitle(self, newValue):
        if isinstance(newValue, str):
            self._title = newValue
        else:
            raise TypeError

    def setUsed(self, newValue):
        if isinstance(newValue, int):
            self._used = newValue
        else:
            raise TypeError

    def setZimbraAccountStatus(self, newValue):
        if newValue == "active" or newValue == "closed":
            self._zimbraAccountStatus = newValue
        else:
            raise TypeError

    def setZimbraFeatureBriefcasesEnabled(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraFeatureBriefcasesEnabled = newValue
        else:
            raise TypeError

    def setZimbraFeatureCalendarEnabled(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraFeatureCalendarEnabled = newValue
        else:
            raise TypeError

    def setZimbraFeatureMailEnabled(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraFeatureMailEnabled = newValue
        else:
            raise TypeError

    def setZimbraFeatureMailForwardingEnabled(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraFeatureMailForwardingEnabled = newValue
        else:
            raise TypeError

    def setZimbraFeatureOptionsEnabled(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraFeatureOptionsEnabled = newValue
        else:
            raise TypeError

    def setZimbraFeatureTasksEnabled(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraFeatureTasksEnabled = newValue
        else:
            raise TypeError

    def setZimbraHideInGal(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraHideInGal = newValue
        else:
            raise TypeError

    def setZimbraMailQuota(self, newValue):
        if isinstance(newValue, int):
            self._zimbraMailQuota = newValue
        else:
            raise TypeError

    def setZimbraMailAlias(self, newValue):
        if isinstance(newValue, list):
            self._zimbraMailAlias = newValue
        else:
            raise TypeError

    def setZimbraMailCanonicalAddress(self, newValue):
        if isinstance(newValue, str):
            if utils.checkIsMailAddress(newValue):
                self._zimbraMailCanonicalAddress = newValue
        else:
            raise TypeError

    def setZimbraLastLogonTimestamp(self, newValue):
        if isinstance(newValue, str):
            self._zimbraLastLogonTimestamp = newValue
        else:
            raise TypeError

    def setZimbraNotes(self, newValue):
        if isinstance(newValue, str):
            self._zimbraNotes = newValue
        else:
            raise TypeError

    def setZimbraPasswordMustChange(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraPasswordMustChange = newValue
        else:
            raise TypeError

    def setZimbraPrefFromDisplay(self, newValue):
        if isinstance(newValue, bool):
            if utils.checkIsMailAddress(newValue):
                self._zimbraPrefFromDisplay = newValue
        else:
            raise TypeError

    def setZimbraPrefMailForwardingAddress(self, newValue):
        if isinstance(newValue, bool):
            if utils.checkIsMailAddress(newValue):
                self._zimbraPrefMailForwardingAddress = newValue
        else:
            raise TypeError

    def setZimbraPrefMailLocalDeliveryDisabled(self, newValue):
        if isinstance(newValue, bool):
            self._zimbraPrefMailLocalDeliveryDisabled = newValue
        else:
            raise TypeError

    def setZimbraCOSId(self, newValue):
        if isinstance(newValue, str):
            self._zimbraCOSId = newValue
        else:
            raise TypeError

    def addZimbraZimletAvailableZimlets(self, newValue):
        if isinstance(newValue, str):
            if self._zimbraZimletAvailableZimlets is None:
                self._zimbraZimletAvailableZimlets = []
            if newValue not in self._zimbraZimletAvailableZimlets:
                self._zimbraZimletAvailableZimlets.append(newValue)
        else:
            raise TypeError

    def removeZimbraZimletAvailableZimlets(self, valueToRemove):
        if isinstance(valueToRemove, str):
            if valueToRemove in self._zimbraZimletAvailableZimlets:
                self._zimbraZimletAvailableZimlets.remove(valueToRemove)
        else:
            raise TypeError

