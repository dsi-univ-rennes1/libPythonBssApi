import pytest
from requests.models import Response
from unittest.mock import MagicMock

from lib_Partage_BSS.exceptions import DomainException
from lib_Partage_BSS.exceptions.BSSConnexionException import BSSConnexionException

import time as timer
import hmac

from lib_Partage_BSS.services import BSSConnexion


@pytest.fixture()
def create_connexion():
    con = BSSConnexion()
    con.setDomainKey({"domain.com": "keyDeTest"})
    con.setDomainKey({"autre.com": "keyDeTest"})
    con.ttl = 10
    return con


def mock_response():
    class MockResponse(Response):

        def __init__(self):
            Response.__init__(self)
            self.status_code = 200
            self._text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>BSSToken</token>\n</Response>\n"

    return MockResponse


def test_getToken_casNormal(mocker):
    con = create_connexion()
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>tokenDeTest</token>\n</Response>\n"
    with mocker.patch('requests.post', return_value=response):
        assert con.token("domain.com") == "tokenDeTest"
    BSSConnexion.instance = None


def test_getToken_casNormalSurAutreDomain(mocker):
    con = create_connexion()
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>tokenDeTest</token>\n</Response>\n"
    with mocker.patch('requests.post', return_value=response):
        assert con.token("autre.com") == "tokenDeTest"
    BSSConnexion.instance = None


def test_getToken_casPreAuthEchec(mocker):
    with pytest.raises(BSSConnexionException):
        con = create_connexion()
        response = MagicMock(Response)
        response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">2</status>\n  <message>Echec de la preauthentification</message>\n  <token>tokenDeTestEchec</token>\n</Response>\n"
        with mocker.patch('requests.post', return_value=response):
            token = con.token("domain.com")
            print(token)
    BSSConnexion.instance = None


def test_getToken_casDomainNonString(mocker):
    with pytest.raises(TypeError):
        con = create_connexion()
        response = MagicMock(Response)
        response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">2</status>\n  <message>Echec de la preauthentification</message>\n  <token>tokenDeTestEchec</token>\n</Response>\n"
        with mocker.patch('requests.post', return_value=response):
            token = con.token(0)
    BSSConnexion.instance = None


def test_getToken_casDomainNonValide(mocker):
    with pytest.raises(DomainException):
        con = create_connexion()
        response = MagicMock(Response)
        response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">2</status>\n  <message>Echec de la preauthentification</message>\n  <token>tokenDeTestEchec</token>\n</Response>\n"
        with mocker.patch('requests.post', return_value=response):
            token = con.token("domain")
    BSSConnexion.instance = None


def test_getToken_casDomainNonPresentDansConfig(mocker):
    with pytest.raises(DomainException):
        con = create_connexion()
        response = MagicMock(Response)
        response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">2</status>\n  <message>Echec de la preauthentification</message>\n  <token>tokenDeTestEchec</token>\n</Response>\n"
        with mocker.patch('requests.post', return_value=response):
            token = con.token("domain.fr")
    BSSConnexion.instance = None

def test_getToken_4minApresCreation(mocker):
    con = create_connexion()
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>tokenDeTest</token>\n</Response>\n"
    with mocker.patch('requests.post', return_value=response):
        token = con.token("domain.com")
        mocker.spy(hmac, 'new')
        timer.sleep(int( con.ttl * .8 ))
        token = con.token("domain.com")
        assert hmac.new.call_count == 0
    BSSConnexion.instance = None


def test_getToken_5minApresCreation(mocker):
    con = create_connexion()
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>tokenDeTest</token>\n</Response>\n"
    with mocker.patch('requests.post', return_value=response):
        token = con.token("domain.com")
        mocker.spy(hmac, 'new')
        timer.sleep(con.ttl)
        token = con.token("domain.com")
        assert hmac.new.call_count == 1
    BSSConnexion.instance = None
