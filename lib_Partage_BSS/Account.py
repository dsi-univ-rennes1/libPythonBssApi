import hashlib
import re

from lib_Partage_BSS.GlobalService import GlobalService
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.exceptions.ServiceException import ServiceException


class Account(GlobalService):
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
    :ivar _eppn: EduPersonPrincipalName l'identifiant fondation du compte
    :ivar _givenName: Prénom de famille de la personne
    :ivar _displayName: Prénom Nom de la personne
    :ivar _businessCategory: ...
    :ivar _sn: Nom de la personne
    :ivar _st:
    :ivar _street: Rue de la personne
    :ivar _telehoneNumber: Numéro de téléphone de la personne
    :ivar _title: ...
    :ivar _zimbraAccountStatus: Etat du compte défaut active (active,closed)
    :ivar _zimbraFeatureBriefcasesEnabled: ...
    :ivar _zimbraFeatureCalendarEnabled: ...
    :ivar _zimbraFeatureMailEnabled: ...
    :ivar _zimbraFeatureMailForwardingEnabled: Permettre à l’utilisateur d’indiquer une adresse de redirection (TRUE,FALSE)
    :ivar _zimbraFeatureOptionsEnabled: ...
    :ivar _zimbraFeatureTasksEnabled: ...
    :ivar _zimbraHideInGal: Masquer dans la GAL (TRUE,FALSE)
    :ivar _zimbraLastLogonTimestamp: Timestamp de la dernière connection au compte
    :ivar _zimbraMailQuota: ...
    :ivar _zimbraNotes: ...
    :ivar _zimbraPasswordMustChange: Forcer le changement de mot de passe à la prochaine connection (TRUE,FALSE)
    :ivar _zimbraPrefMailForwardingAddress: Adresse de redirection saisie par l’utilisateur
    :ivar _zimbraPrefMailLocalDeliveryDisabled: Ne pas conserver de copie des mails sur le client local
    :ivar _zimbraMailCanonicalAddress: Adresse email visible pour les messages sortants
    :ivar _zimbraPrefFromDisplay: Adresse email visible pour les messages sortants
    :ivar _zimbraCOSId: Id de la classe de Service du compte
    :ivar _zimbraZimletAvailableZimlets: Les zimlets disponible pour le compte
    """
    def __init__(self, connexion, name):
        if re.match(".+@.+", name):
            GlobalService.__init__(self, connexion, name)
            self._id = ""
            self._admin = ""
            self._businessCategory = ""
            self._co = ""
            self._company = ""
            self._description = ""
            self._displayName = ""
            self._eppn = ""
            self._facsimileTelephoneNumber = ""
            self._givenName = ""
            self._homePhone = ""
            self._initials = ""
            self._l = ""
            self._mavTransformation = ""
            self._mavRedirection = ""
            self._mobile = ""
            self._pager = ""
            self._postalCode = ""
            self._quota = 0
            self._sn = ""
            self._st = ""
            self._street = ""
            self._telehoneNumber = ""
            self._title = ""
            self._used = 0
            self._zimbraAccountStatus = ""
            self._zimbraFeatureBriefcasesEnabled = ""
            self._zimbraFeatureCalendarEnabled = ""
            self._zimbraFeatureMailEnabled = ""
            self._zimbraFeatureMailForwardingEnabled = ""
            self._zimbraFeatureOptionsEnabled = ""
            self._zimbraFeatureTasksEnabled = ""
            self._zimbraHideInGal = ""
            self._zimbraLastLogonTimestamp = ""
            self._zimbraMailQuota = ""
            self._zimbraNotes = ""
            self._zimbraPasswordMustChange = ""
            self._zimbraPrefMailForwardingAddress = ""
            self._zimbraPrefMailLocalDeliveryDisabled = ""
            self._zimbraMailCanonicalAddress = ""
            self._zimbraPrefFromDisplay = ""
            self._zimbraCOSId = ""
            self._zimbraZimletAvailableZimlets = []

        else:
            raise NameException("Le nom donné n'est pas une adresse mail")

    def getAccount(self):
        data = {
            "name": self._name
        }
        response = self.callMethod("GetAccount", data)
        if response["status"] == 0:
            account= response["account"]
            print(account)
            accountKeys = account.keys()
            if "id" in accountKeys:
                self._id = account["id"]
            if "admin" in accountKeys:
                self._admin = account["admin"]
            if "businessCategory" in accountKeys:
                self._businessCategory = account["businessCategory"]
            if "carLicense" in accountKeys:
                self._eppn = account["carLicense"]
            if "co" in accountKeys:
                self._co = account["co"]
            if "company" in accountKeys:
                self._company = account["company"]
            if "description" in accountKeys:
                self._description = account["description"]
            if "displayName" in accountKeys:
                self._displayName = account["displayName"]
            if "facsimileTelephoneNumber" in accountKeys:
                self._facsimileTelephoneNumber = account["facsimileTelephoneNumber"]
            if "givenName" in accountKeys:
                self._givenName = account["givenName"]
            if "homePhone" in accountKeys:
                self._homePhone = account["homePhone"]
            if "initials" in accountKeys:
                self._initials = account["initials"]
            if "l" in accountKeys:
                self._l = account["l"]
            if "mav-transformation" in accountKeys:
                self._mavTransformation = account["mav-transformation"]
            if "mav-redirection" in accountKeys:
                self._mavRedirection = account["mav-redirection"]
            if "mobile" in accountKeys:
                self._mobile = account["mobile"]
            if "pager" in accountKeys:
                self._pager = account["pager"]
            if "postalCode" in accountKeys:
                self._postalCode = account["postalCode"]
            if "quota" in accountKeys:
                self._quota = account["quota"]
            if "sn" in accountKeys:
                self._sn = account["sn"]
            if "st" in accountKeys:
                self._st = account["st"]
            if "street" in accountKeys:
                self._street = account["street"]
            if "telehoneNumber" in accountKeys:
                self._telehoneNumber = account["telehoneNumber"]
            if "title" in accountKeys:
                self._title = account["title"]
            if "used" in accountKeys:
                self._used = account["used"]
            if "zimbraAccountStatus" in accountKeys:
                self._zimbraAccountStatus = account["zimbraAccountStatus"]
            if "zimbraCOSId" in accountKeys:
                self._zimbraCOSId = account["zimbraCOSId"]
            if "zimbraFeatureBriefcasesEnabled" in accountKeys:
                if account["zimbraFeatureBriefcasesEnabled"] == "TRUE":
                    self._zimbraFeatureBriefcasesEnabled = True
                else:
                    self._zimbraFeatureBriefcasesEnabled = False
            if "zimbraFeatureCalendarEnabled" in accountKeys:
                if account["zimbraFeatureCalendarEnabled"] == "TRUE":
                    self._zimbraFeatureCalendarEnabled = True
                else:
                    self._zimbraFeatureCalendarEnabled = False
            if "zimbraFeatureMailEnabled" in accountKeys:
                if account["zimbraFeatureMailEnabled"] == "TRUE":
                    self._zimbraFeatureMailEnabled = True
                else:
                    self._zimbraFeatureMailEnabled = False
            if "zimbraFeatureMailForwardingEnabled" in accountKeys:
                if account["zimbraFeatureMailForwardingEnabled"] == "TRUE":
                    self._zimbraFeatureMailForwardingEnabled = True
                else:
                    self._zimbraFeatureMailForwardingEnabled = False
            if "zimbraFeatureOptionsEnabled" in accountKeys:
                if account["zimbraFeatureOptionsEnabled"] == "TRUE":
                    self._zimbraFeatureOptionsEnabled = True
                else:
                    self._zimbraFeatureOptionsEnabled = False
            if "zimbraFeatureTasksEnabled" in accountKeys:
                if account["zimbraFeatureTasksEnabled"] == "TRUE":
                    self._zimbraFeatureTasksEnabled = True
                else:
                    self._zimbraFeatureTasksEnabled = False
            if "zimbraHideInGal" in accountKeys:
                if account["zimbraHideInGal"] == "TRUE":
                    self._zimbraHideInGal = True
                else:
                    self._zimbraHideInGal = False
            if "zimbraLastLogonTimestamp" in accountKeys:
                self._zimbraLastLogonTimestamp = account["zimbraLastLogonTimestamp"]
            if "zimbraMailQuota" in accountKeys:
                self._zimbraMailQuota = account["zimbraMailQuota"]
            if "zimbraNotes" in accountKeys:
                self._zimbraNotes = account["zimbraNotes"]
            if "zimbraPasswordMustChange" in accountKeys:
                if account["zimbraPasswordMustChange"] == "TRUE":
                    self._zimbraPasswordMustChange = True
                else:
                    self._zimbraPasswordMustChange = False
            if "zimbraPrefMailLocalDeliveryDisabled" in accountKeys:
                if account["zimbraPrefMailLocalDeliveryDisabled"] == "TRUE":
                    self._zimbraPrefMailLocalDeliveryDisabled = True
                else:
                    self._zimbraPrefMailLocalDeliveryDisabled = False
            if "zimbraPrefMailForwardingAddress" in accountKeys:
                self._zimbraPrefMailForwardingAddress = account["zimbraPrefMailForwardingAddress"]
            if "zimbraMailCanonicalAddress" in accountKeys:
                self._zimbraMailCanonicalAddress = account["zimbraMailCanonicalAddress"]
            if "zimbraPrefFromDisplay" in accountKeys:
                self._zimbraPrefFromDisplay = account["zimbraPrefFromDisplay"]
            if "zimbraZimletAvailableZimlets" in accountKeys:
                self._zimbraZimletAvailableZimlets = account["zimbraZimletAvailableZimlets"]["zimbraZimletAvailableZimlet"]
        else:
            raise ServiceException(response["status"], response["message"])

    def createAccount(self,userPassword):
        data = {
            "name": self._name,
            "password": "",
            "userPassword": userPassword,
            "zimbraHideInGal": "FALSE"
        }
        response = self.callMethod("CreateAccount", data)
        if response["status"] != 0:
            raise ServiceException(response["status"], response["message"])

    def deleteAccount(self):
        data = {
            "name": self._name
        }
        response = self.callMethod("DeleteAccount", data)
        if response["status"] != 0:
            raise ServiceException(response["status"], response["message"])

    def getId(self):
        return self._id

    def getAdmin(self):
        return self._admin

    def getBusinessCategory(self):
        return self._businessCategory

    def getCo(self):
        return self._co

    def getCompany(self):
        return self._company

    def getDisplayName(self):
        return self._displayName

    def getEppn(self):
        return self._eppn

    def getFacsimileTelephoneNumber(self):
        return self._facsimileTelephoneNumber

    def getGivenName(self):
        return self._givenName

    def getHomePhone(self):
        return self._homePhone

    def getInitials(self):
        return self._initials

    def getL(self):
        return  self._l

    def getMavTransformation(self):
        return self._mavTransformation

    def getMavRedirection(self):
        return self._mavRedirection

    def getMobile(self):
        return self._mobile

    def getPager(self):
        return self._pager

    def getPosyalCode(self):
        return self._postalCode

    def getQuota(self):
        return self._quota

    def getSn(self):
        return self._sn

    def getSt(self):
        return self._st

    def getStreet(self):
        return self._street

    def getTelephoneNumber(self):
        return self._telehoneNumber

    def getTitle(self):
        return self._title

    def getUsed(self):
        return self._used

    def getZimbraAccountStatus(self):
        return self._zimbraAccountStatus

    def getZimbraFeatureBriefcasesEnabled(self):
        return self._zimbraFeatureBriefcasesEnabled

    def getZimbraFeatureCalendarEnabled(self):
        return self._zimbraFeatureCalendarEnabled

    def getZimbraFeatureMailEnabled(self):
        return self._zimbraFeatureMailEnabled

    def getZimbraFeatureMailForwardingEnabled(self):
        return self._zimbraFeatureMailForwardingEnabled

    def getZimbraFeatureOptionsEnabled(self):
        return self._zimbraFeatureOptionsEnabled

    def getZimbraFeatureTasksEnabled(self):
        return self._zimbraFeatureTasksEnabled

    def getZimbraHideInGal(self):
        return self._zimbraHideInGal

    def getZimbraLastLogonTimestamp(self):
        return self._zimbraLastLogonTimestamp

    def getZimbraMailQuota(self):
        return self._zimbraMailQuota

    def getZimbraCanonicalAddress(self):
        return self._zimbraMailCanonicalAddress

    def getZimbraNotes(self):
        return self._zimbraNotes

    def getZimbraPasswordMustChange(self):
        return self._zimbraPasswordMustChange

    def getZimbraPrefFromDisplay(self):
        return self._zimbraPrefFromDisplay

    def getZimbraPrefMailForwardingAddress(self):
        return self._zimbraPrefMailForwardingAddress

    def getZimbraPrefMailLocalDeliveryDisabled(self):
        return self._zimbraPrefMailLocalDeliveryDisabled

    def getZimbraCOSId(self):
        return self._zimbraCOSId

    def getZimbraZimletAvailableZimlets(self):
        return self._zimbraZimletAvailableZimlets

    def setId(self, newValue):
        self._id = newValue

    def setAdmin(self, newValue):
        self._admin = newValue

    def setBusinessCategory(self, newValue):
        self._businessCategory = newValue

    def setCo(self, newValue):
        self._co = newValue

    def setCompany(self, newValue):
        self._company = newValue

    def setDisplayName(self, newValue):
        self._displayName = newValue

    def setEppn(self, newValue):
        self._eppn = newValue

    def setFacsimileTelephoneNumber(self, newValue):
        self._facsimileTelephoneNumber = newValue

    def setGivenName(self, newValue):
        self._givenName = newValue

    def setHomePhone(self, newValue):
        self._homePhone = newValue

    def setInitials(self, newValue):
        self._initials = newValue

    def setL(self, newValue):
        self._l = newValue

    def setMavTransformation(self, newValue):
        self._mavTransformation = newValue

    def setMavRedirection(self, newValue):
        self._mavRedirection = newValue

    def setMobile(self, newValue):
        self._mobile = newValue

    def setPager(self, newValue):
        self._pager = newValue

    def setPosyalCode(self, newValue):
        self._postalCode = newValue

    def setQuota(self, newValue):
        self._quota = newValue

    def setSn(self, newValue):
        self._sn = newValue

    def setSt(self, newValue):
        self._st = newValue

    def setStreet(self, newValue):
        self._street = newValue

    def setTelephoneNumber(self, newValue):
        self._telehoneNumber = newValue

    def setTitle(self, newValue):
        self._title = newValue

    def setUsed(self, newValue):
        self._used = newValue

    def setZimbraAccountStatus(self, newValue):
        self._zimbraAccountStatus = newValue

    def setZimbraFeatureBriefcasesEnabled(self, newValue):
        self._zimbraFeatureBriefcasesEnabled = newValue

    def setZimbraFeatureCalendarEnabled(self, newValue):
        self._zimbraFeatureCalendarEnabled = newValue

    def setZimbraFeatureMailEnabled(self, newValue):
        self._zimbraFeatureMailEnabled = newValue

    def setZimbraFeatureMailForwardingEnabled(self, newValue):
        self._zimbraFeatureMailForwardingEnabled = newValue

    def setZimbraFeatureOptionsEnabled(self, newValue):
        self._zimbraFeatureOptionsEnabled = newValue

    def setZimbraFeatureTasksEnabled(self, newValue):
        self._zimbraFeatureTasksEnabled = newValue

    def setZimbraHideInGal(self, newValue):
        self._zimbraHideInGal = newValue

    def setZimbraLastLogonTimestamp(self, newValue):
        self._zimbraLastLogonTimestamp = newValue

    def setZimbraMailQuota(self, newValue):
        self._zimbraMailQuota = newValue

    def setZimbraCanonicalAddress(self, newValue):
        self._zimbraMailCanonicalAddress = newValue

    def setZimbraNotes(self, newValue):
        self._zimbraNotes = newValue

    def setZimbraPasswordMustChange(self, newValue):
        self._zimbraPasswordMustChange = newValue

    def setZimbraPrefFromDisplay(self, newValue):
        self._zimbraPrefFromDisplay = newValue

    def setZimbraPrefMailForwardingAddress(self, newValue):
        self._zimbraPrefMailForwardingAddress = newValue

    def setZimbraPrefMailLocalDeliveryDisabled(self, newValue):
        self._zimbraPrefMailLocalDeliveryDisabled = newValue

    def setZimbraCOSId(self, newValue):
        self._zimbraCOSId = newValue

    def setZimbraZimletAvailableZimlets(self, newValue):
        self._zimbraZimletAvailableZimlets = newValue