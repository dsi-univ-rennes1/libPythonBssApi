import pytest
from requests.models import Response
from unittest.mock import MagicMock
from lib_Partage_BSS.exceptions.BSSConnexionException import BSSConnexionException
from lib_Partage_BSS.utils.BSSConnexion import BSSConnexion
import time as timer
import hmac


@pytest.fixture()
def create_connexion():
    return BSSConnexion("ur1.fr", "key")


def mock_response():
    class MockResponse(Response):

        def __init__(self):
            Response.__init__(self)
            self.status_code = 200
            self._text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>BSSToken</token>\n</Response>\n"

    return MockResponse


def test_getUrl_casNormal():
    con = create_connexion()
    assert con.url == "https://api.partage.renater.fr/service/domain/"


def test_getDomain_casNormal():
    con = create_connexion()
    assert con.domain == "ur1.fr"


def test_getToken_casNormal(mocker):
    con = create_connexion()
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>tokenDeTest</token>\n</Response>\n"
    with mocker.patch('requests.post', return_value=response):
        assert con.token == "tokenDeTest"


def test_getToken_casPreAuthEchec(mocker):
    with pytest.raises(BSSConnexionException):
        con = create_connexion()
        response = MagicMock(Response)
        response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">2</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>BSSToken</token>\n</Response>\n"
        with mocker.patch('requests.post', return_value=response):
            token = con.token


def test_getToken_4minApresCreation(mocker):
    con = create_connexion()
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>BSSToken</token>\n</Response>\n"
    with mocker.patch('requests.post', return_value=response):
        token = con.token
        mocker.spy(hmac, 'new')
        timer.sleep(240)
        token = con.token
        assert hmac.new.call_count == 0


def test_getToken_5minApresCreation(mocker):
    con = create_connexion()
    response = MagicMock(Response)
    response.text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <status type=\"integer\">0</status>\n  <message>Op\xc3\xa9ration r\xc3\xa9alis\xc3\xa9e avec succ\xc3\xa8s !</message>\n  <token>BSSToken</token>\n</Response>\n"
    with mocker.patch('requests.post', return_value=response):
        token = con.token
        mocker.spy(hmac, 'new')
        timer.sleep(300)
        token = con.token
        assert hmac.new.call_count == 1
