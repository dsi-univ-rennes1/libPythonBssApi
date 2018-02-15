# -*-coding:Latin-1 -*

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
    def __init__(self, connexion, name):
        if re.match(".+@.+", name):
            GlobalService.__init__(self, connexion, name)
            self._id = None
            self._admin = None
            self._businessCategory = None
            self._co = None
            self._company = None
            self._description = None
            self._displayName = None
            self._eppn = None
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
            self._telehoneNumber = None
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

    def getAccount(self):
        """
        Méthide permettant de récuperer les informations d'un compte via l'API BSS
        :return: Le compte récupéré
        """
        data = {
            "name": self._name
        }
        response = self.callMethod("GetAccount", data)
        if response["status"] == 0:
            account= response["account"]
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
            if "zimbraMailAlias" in accountKeys:
                self._zimbraMailAlias = account["zimbraMailAlias"]["zimbraMailAlias"]
            if "zimbraMailCanonicalAddress" in accountKeys:
                self._zimbraMailCanonicalAddress = account["zimbraMailCanonicalAddress"]
            if "zimbraPrefFromDisplay" in accountKeys:
                self._zimbraPrefFromDisplay = account["zimbraPrefFromDisplay"]
            if "zimbraZimletAvailableZimlets" in accountKeys:
                self._zimbraZimletAvailableZimlets = account["zimbraZimletAvailableZimlets"]["zimbraZimletAvailableZimlet"]
        else:
            raise ServiceException(response["status"], response["message"])

    def createAccount(self,userPassword, cosId):
        """
        Méthode permettant de créer un compte via l'API BSS en lui passant en paramètre l'empreinte du mot de passe (SSHA) et le cosId
        :param userPassword: le mot de passe de l'utilisateur hashé en SSHA1
        :param cosId: l'identifiant du cosId à appliquer pour le compte
        :return:
        """
        if userPassword[:6] == "{SSHA}":
            data = {
                "name": self._name,
                "password": "",
                "userPassword": userPassword,
                "zimbraHideInGal": "FALSE",
                "zimbraCOSId": cosId
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

    def modifyAccount(self):
        data = {
            "name": self._name,
            "co": self._co,
            "company": self._company,
            "description": self._description,
            "displayName": self._displayName,
            "carLicense": self._eppn,
            "facsimileTelephoneNumber": self._facsimileTelephoneNumber,
            "givenName": self._givenName,
            "homePhone": self._homePhone,
            "initials": self._initials,
            "l": self._l,
            "mav-transformation": self._mavTransformation,
            "mav-redirection": self._mavRedirection,
            "mobile": self._mobile,
            "pager": self._pager,
            "postalCode": self._postalCode,
            "sn": self._sn,
            "st": self._st,
            "street": self._street,
            "telehoneNumber": self._telehoneNumber,
            "title": self._title,
            "zimbraAccountStatus": self._zimbraAccountStatus,
            "zimbraFeatureBriefcasesEnabled": self._zimbraFeatureBriefcasesEnabled,
            "zimbraFeatureCalendarEnabled": self._zimbraFeatureCalendarEnabled,
            "zimbraFeatureMailEnabled": self._zimbraFeatureMailEnabled,
            "zimbraFeatureMailForwardingEnabled": self._zimbraFeatureMailForwardingEnabled,
            "zimbraFeatureOptionsEnabled": self._zimbraFeatureOptionsEnabled,
            "zimbraFeatureTasksEnabled": self._zimbraFeatureTasksEnabled,
            "zimbraHideInGal": self._zimbraHideInGal,
            "zimbraLastLogonTimestamp": self._zimbraLastLogonTimestamp,
            "zimbraMailQuota": self._zimbraMailQuota,
            "zimbraNotes": self._zimbraNotes,
            "zimbraPasswordMustChange": self._zimbraPasswordMustChange,
            "zimbraPrefMailForwardingAddress": self._zimbraPrefMailForwardingAddress,
            "zimbraPrefMailLocalDeliveryDisabled": self._zimbraPrefMailLocalDeliveryDisabled,
            "zimbraMailCanonicalAddress": self._zimbraMailCanonicalAddress,
            "zimbraPrefFromDisplay": self._zimbraPrefFromDisplay,
            "zimbraCOSId": self._zimbraCOSId,
            "zimbraZimletAvailableZimlets": self._zimbraZimletAvailableZimlets
        }
        response = self.callMethod("ModifyAccount", data)
        if response["status"] != 0:
            raise ServiceException(response["status"], response["message"])

    def modifyPassword(self, newUserPassword):
        """
        Pour modifier le mot de passe on n'accept que l'emprunte du mot de passe.
        On commence par faire un SetPassword avec une valeur factise pour forcer la déconnection des session en cours
        On passe ensuite via ModifyAccount l'empreinte du nouveau mot de passe
        :param newUserPassword:
        :return:
        """
        data= {
            "name": self._name,
            "password": "valeurPourDeconnecterLesSessions"
        }
        response = self.callMethod("SetPassword", data)
        if response["status"] != 0:
            raise ServiceException(response["status"], response["message"])
        data = {
            "name": self._name,
            "userPassword": newUserPassword
        }
        response = self.callMethod("ModifyAccount", data)
        if response["status"] != 0:
            raise ServiceException(response["status"], response["message"])

    def addAccountAlias(self, newAlias):
        data = {
            "name": self._name,
            "alias": newAlias
        }
        response = self.callMethod("AddAccountAlias", data)
        if response["status"] != 0:
            raise ServiceException(response["status"], response["message"])

    def deleteAccountAlias(self, aliasToDelete):
        data = {
            "name": self._name,
            "alias": aliasToDelete
        }
        response = self.callMethod("RemoveAccountAlias", data)
        if response["status"] != 0:
            raise ServiceException(response["status"], response["message"])

    def modifyAccountAliases(self, listOfAliases):
        if isinstance(listOfAliases, list):
            for alias in listOfAliases:
                if isinstance(self.getZimbraMailAlias(), list) or isinstance(self.getZimbraMailAlias(), str) :
                    if alias not in self.getZimbraMailAlias():
                        self.addAccountAlias(alias)
                else:
                    self.addAccountAlias(alias)
            if isinstance(self.getZimbraMailAlias(), list):
                for alias in self.getZimbraMailAlias():
                    if alias not in listOfAliases:
                        self.deleteAccountAlias(alias)
            elif isinstance(self.getZimbraMailAlias(), str):
                if self.getZimbraMailAlias() not in listOfAliases:
                    self.deleteAccountAlias(self.getZimbraMailAlias())

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

    def getZimbraMailAlias(self):
        return self._zimbraMailAlias

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

    def setDisplayName(self, newValue):
        if isinstance(newValue, str):
            self._displayName = newValue
        else:
            raise TypeError

    def setEppn(self, newValue):
        if isinstance(newValue, str):
            self._eppn = newValue
        else:
            raise TypeError

    def setFacsimileTelephoneNumber(self, newValue):
        if isinstance(newValue, str):
            if self.chekIsNum(newValue):
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
            if self.chekIsNum(newValue):
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
        if isinstance(newValue, str):
            self._mavTransformation = newValue
        else:
            raise TypeError

    def setMavRedirection(self, newValue):
        if isinstance(newValue, str):
            self._mavRedirection = newValue
        else:
            raise TypeError

    def setMobile(self, newValue):
        if isinstance(newValue, str):
            if self.chekIsNum(newValue):
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
            if self.chekIsNum(newValue):
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
            if self.chekIsNum(newValue):
                self._telehoneNumber = newValue
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

    def activeZimbraAccount(self):
        self._zimbraAccountStatus = "active"

    def closedZimbraAccount(self):
        self._zimbraAccountStatus = "closed"

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

    def setZimbraCanonicalAddress(self, newValue):
        if isinstance(newValue, int):
            if self.checkIsMailAddress(newValue):
                self._zimbraMailCanonicalAddress = newValue
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
            if self.checkIsMailAddress(newValue):
                self._zimbraPrefFromDisplay = newValue
        else:
            raise TypeError

    def setZimbraPrefMailForwardingAddress(self, newValue):
        if isinstance(newValue, bool):
            if self.checkIsMailAddress(newValue):
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

    def setZimbraZimletAvailableZimlets(self, newValue):
        if isinstance(newValue, list):
            self._zimbraZimletAvailableZimlets = newValue
        else:
            raise TypeError

    def chekIsNum(self, value):
        """
        Vérifie si la valeur passé en paramètre est un numéro ou pas (constitué uniquement de digit)
        :param value: la valeur a tester
        :return: True si c'est un numéro False sinon
        """
        return re.match("^[0-9]*$", value)

    def checkIsMailAddress(self,value):
        """
        Vérifie si la valeur passé en paramètre est une adresse mail ou pas (contient une chaine suivi d'un @ suivi d'une chaine suivi d'un point suivi d'une chaine)
        :param value: la valeur a tester
        :return: True si c'est une adresse mail False sinon
        """
        return re.match("^[^\W][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)*\@[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\.[a-zA-Z]{2,4}$", value)

    def changeBooleanToString(self, boolean):
        """
        Permet de changer les booleen True et False en String correspondant entièrement en majuscule.
        :param booleanString: le booleen à changer en String
        :return: "TRUE" ou  "FALSE"
        """
        if isinstance(boolean, bool):
            if boolean:
                return "TRUE"
            else:
                return "FALSE"

    def changeStringToBoolean(self, booleanString):
        """
        Permet de changer les chaines TRUE et FALSE (quelque soit leurs case) en booleen correspondant.
        Renvoie un TypeErreur sinon
        :param booleanString: "TRUE" ou  "FALSE"
        :return: renvoie le booleen correspondant
        """
        if isinstance(booleanString, str):
            if booleanString.upper() == "TRUE":
                return True
            elif booleanString.upper() == "FALSE":
                return False
            else:
                raise TypeError()
