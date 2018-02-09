from unittest.mock import MagicMock

import pytest
from requests import Response

from lib_Partage_BSS.Account import Account
from lib_Partage_BSS.exceptions.NameException import NameException
from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS.utils.BSSConnexion import BSSConnexion


@pytest.fixture()
def create_connexion():
    return BSSConnexion("domain.com", "key")


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

def test_init_cas_nom_vallide():
    con = create_connexion()
    account = Account(con, "test@domain.com")
    assert account.getName() == "test@domain.com"

def test_init_cas_nom_non_vallide():
    with pytest.raises(NameException):
        con = create_connexion()
        account = Account(con, "test")

def test_getAccount_cas_compte_existant(mocker):
    con = create_connexion()
    account = Account(con, "test@domain.com")
    response = initGoodResponse()
    with mocker.patch('requests.post', return_value=response):
        with mocker.patch.object(BSSConnexion, 'token', return_value="test"):
            account.getAccount()
            assert account.getName() == "test@domain.com"
            assert account.getEppn() == "EPPN"
            assert account.getZimbraCOSId() == "testCOSId"
            print(account.getZimbraZimletAvailableZimlets()[0])

def test_getAccount_cas_compte_inexistant(mocker):
    with pytest.raises(ServiceException):
        con = create_connexion()
        account = Account(con, "test@domain.com")
        response = initBadResponse()
        with mocker.patch('requests.post', return_value=response):
            with mocker.patch.object(BSSConnexion, 'token', return_value="test"):
                account.getAccount()