import pytest

from lib_Partage_BSS.exceptions import DomainException
from lib_Partage_BSS.exceptions.BSSConnexionException import BSSConnexionException
import re
import time as timer
from lib_Partage_BSS.services import BSSConnexion

def create_connexion(config):
    timer.sleep(1)
    con = BSSConnexion()
    if 'bss_url' in config:
        con.url = config['bss_url']
    con.setDomainKey({config['bss_domain']: config['bss_domain_key']})
    return BSSConnexion()

def close_connexion(con):
    con.instance = None

def test_getToken_casNormal(test_config):
    con = create_connexion(test_config)
    assert re.match("[0-9a-z]{32}", con.token(test_config['bss_domain']))
    close_connexion(con)

def test_getToken_casDomainFaux(test_config):
    con = create_connexion(test_config)
    with pytest.raises(DomainException):
       con.token("not_a_domain")
    close_connexion(con)

def test_getToken_casDomainNonPresent(test_config):
    con = create_connexion(test_config)
    with pytest.raises(DomainException):
        token = con.token("unknown_domain")

def test_getToken_8sApresCreation(test_config):
    con = create_connexion(test_config)
    token = con.token(test_config['bss_domain'])
    timer.sleep(8)
    token2 = con.token(test_config['bss_domain'])
    assert token == token2
    close_connexion(con)

@pytest.mark.skip(reason="ça prend trop de temps...")
def test_getToken_5minApresCreation(test_config):
    con = create_connexion(test_config)
    token = con.token(test_config['bss_domain'])
    timer.sleep(5 * 60)
    token2 = con.token(test_config['bss_domain'])
    assert token != token2
    close_connexion(con)


