import re

from lib_Partage_BSS.GlobalService import GlobalService
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.exceptions.ServiceException import ServiceException


class Account(GlobalService):

    def __init__(self, connexion, name):
        if re.match(".+@.+", name):
            GlobalService.__init__(self, connexion, name)
            self._id = ""
            self._admin = ""
            self._co = ""
            self._company = ""
            self._description = ""
            self._facsimileTelephoneNumber = ""
            self._homePhone = ""
            self._initials = ""
            self._l = ""
            self._mavTransformation = ""
            self._mavRedirection = ""
            self._mobile = ""
            self._pager = ""
            self._postalCode = ""
            self._used = 0
            self._quota = 0
            self._eppn = ""
            self._givenName = ""
            self._displayName = ""
            self._businessCategory = ""
            self._sn = ""
            self._st = ""
            self._street = ""
            self._telehoneNumber = ""
            self._title = ""
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
            raise ServiceException(response["message"])

    def getId(self):
        return self._id

    def getAdmin(self):
        return self._admin

    def getMavTransformation(self):
        return self._mavTransformation

    def getMavRedirection(self):
        return self._mavRedirection

    def getUsed(self):
        return self._used

    def getQuota(self):
        return self._quota

    def getEppn(self):
        return self._eppn

    def getDisplayName(self):
        return self._displayName

    def getGivenName(self):
        return self._givenName

    def getBusinessCategory(self):
        return self._businessCategory

    def getSn(self):
        return self._sn

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

    def getZimbraPrefMailLocalDeliveryDisabled(self):
        return self._zimbraPrefMailLocalDeliveryDisabled

    def getZimbraCOSId(self):
        return self._zimbraCOSId

    def getZimbraZimletAvailableZimlets(self):
        return self._zimbraZimletAvailableZimlets
