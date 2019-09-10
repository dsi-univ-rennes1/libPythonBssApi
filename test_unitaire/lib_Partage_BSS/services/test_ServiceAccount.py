from unittest.mock import MagicMock

import pytest
from requests import Response

from lib_Partage_BSS.models.Account import Account
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.exceptions.DomainException import DomainException
from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS.exceptions.TmpServiceException import TmpServiceException
from lib_Partage_BSS.exceptions.NotFoundException import NotFoundException
from lib_Partage_BSS.services import AccountService, BSSConnexion, BSSConnexionService


@pytest.fixture()
def initGoodResponse():
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                    "<Response>" \
                    "   <status type=\"integer\">0</status>" \
                    "   <message>Opération réalisée avec succès !</message>" \
                    "   <account>" \
                    "       <name>test@domain.com</name>" \
                    "       <id>idTest</id>" \
                    "       <admin>DOMAIN</admin>" \
                    "       <mav-transformation>FALSE</mav-transformation>" \
                    "       <mav-redirection></mav-redirection>" \
                    "       <used type=\"integer\">0</used>" \
                    "       <quota type=\"integer\">0</quota>" \
                    "       <carLicense>EPPN</carLicense>" \
                    "       <givenName>prenomTest</givenName>" \
                    "       <zimbraFeatureMailForwardingEnabled>TRUE</zimbraFeatureMailForwardingEnabled>" \
                    "       <displayName>Rémi Peillet</displayName>" \
                    "       <businessCategory>1</businessCategory>" \
                    "       <zimbraFeatureCalendarEnabled>TRUE</zimbraFeatureCalendarEnabled>" \
                    "       <zimbraAccountStatus>active</zimbraAccountStatus>" \
                    "       <zimbraFeatureContactsEnabled>TRUE</zimbraFeatureContactsEnabled>" \
                    "       <zimbraLastLogonTimestamp>20180131091551Z</zimbraLastLogonTimestamp>" \
                    "       <zimbraFeatureOptionsEnabled>TRUE</zimbraFeatureOptionsEnabled>" \
                    "       <zimbraFeatureTasksEnabled>TRUE</zimbraFeatureTasksEnabled>" \
                    "       <zimbraPrefMailLocalDeliveryDisabled>FALSE</zimbraPrefMailLocalDeliveryDisabled>" \
                    "       <zimbraMailQuota>0</zimbraMailQuota>" \
                    "       <sn>nomTest</sn>" \
                    "       <zimbraCOSId>testCOSId</zimbraCOSId>" \
                    "       <zimbraZimletAvailableZimlets type=\"array\">" \
                    "         <zimbraZimletAvailableZimlet>com_zimbra_attachmail</zimbraZimletAvailableZimlet>" \
                    "         <zimbraZimletAvailableZimlet>com_zimbra_srchhighlighter</zimbraZimletAvailableZimlet>" \
                    "         <zimbraZimletAvailableZimlet>com_zimbra_url</zimbraZimletAvailableZimlet>" \
                    "         <zimbraZimletAvailableZimlet>com_zimbra_email</zimbraZimletAvailableZimlet>" \
                    "         <zimbraZimletAvailableZimlet>com_zimbra_ymemoticons</zimbraZimletAvailableZimlet>" \
                    "         <zimbraZimletAvailableZimlet>com_zimbra_date</zimbraZimletAvailableZimlet>" \
                    "         <zimbraZimletAvailableZimlet>com_zimbra_attachcontacts</zimbraZimletAvailableZimlet>" \
                    "       </zimbraZimletAvailableZimlets>" \
                    "       <zimbraFeatureBriefcasesEnabled>TRUE</zimbraFeatureBriefcasesEnabled>" \
                    "       <zimbraHideInGal>FALSE</zimbraHideInGal>" \
                    "       <zimbraFeatureMailEnabled>TRUE</zimbraFeatureMailEnabled>" \
                    "   </account>" \
                    "</Response>"
    return response


@pytest.fixture()
def initBadResponse():
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                    "<Response>" \
                    "   <status type=\"integer\">2</status>" \
                    "   <message>Opération réalisée avec succès !</message>" \
                    "</Response>"
    return response

@pytest.fixture()
def create_connexion():
    con = BSSConnexion()
    con.setDomainKey({"domain.com": "keyDeTest"})
    return con

def test_init_cas_nom_vallide():
    account = Account("test@domain.com")
    assert account.name == "test@domain.com"


def test_init_cas_nom_non_vallide():
    with pytest.raises(NameException):
        account = Account("test")


def test_getAccount_cas_compte_existant(mocker):
    response = initGoodResponse()
    con = create_connexion()

    with mocker.patch('requests.post', return_value=response):
        with mocker.patch.object(con, 'token', return_value="test"):
            account = AccountService.getAccount("test@domain.com")
            assert account.name == "test@domain.com"
            print(account.carLicense)
            assert account.carLicense == "EPPN"
            assert account.zimbraCOSId == "testCOSId"


def test_getAccount_cas_compte_inexistant(mocker):
    with pytest.raises(ServiceException):
        response = initBadResponse()
        con = create_connexion()
        with mocker.patch('requests.post', return_value=response):
            with mocker.patch.object(con, 'token', return_value="test"):
                AccountService.getAccount("test@domain.com")


