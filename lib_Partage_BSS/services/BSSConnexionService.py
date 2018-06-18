# -*-coding:utf-8 -*
import json
import hmac
import hashlib
from time import time

from lib_Partage_BSS import utils
from lib_Partage_BSS.exceptions import BSSConnexionException, DomainException
from lib_Partage_BSS.utils.BSSRequest import postBSS


class BSSConnexion(object):
    """
    Classe permettant de récuperer un token d'une durée de vie de 5min auprès de l'API BSS Partage.
    Elle regenère un token lorsque celui-ci est sur le point d'expirer

    :ivar _domain: Le domaine cible
    :ivar _key: La clé associée au domaine
    :ivar _timestampOfLastToken: Le timestamp auquel on à obtenue notre dernier token. Permet de renouveller le token avant expiration
    :ivar _token: Le token obtenu via l'API pour utiliser les autres méthodes de l'API
    :ivar _url: L'url vers l'API BSS Partage (https://api.partage.renater.fr/service/domain/)
    :ivar _ttl: le délai d'expiration des tokens reçus (300 secondes par défaut)
    """
    class __BSSConnexion:

        def __init__(self):
            """Constructeur de BSS connexion

               Arguments :
                    domain(string): Le domaine cible
                    key(string): La clé associée au domaine

                Retour :
                    BBSConnexion : l'objet contenant tous les paramètres de connexion

                Exemple d'utilisation :
                >>>BSSConnexion("domain.com","6b7ead4bd425836e8cf0079cd6c1a05acc127acd07c8ee4b61023e19250e929c")
            """
            self._domain = ""
            self._key = {}
            """La clé associés au domaine"""
            self._timestampOfLastToken = {}
            """Le timestamp auquel on a obtenu le dernier token. Permet de renouveller le token avant expiration"""
            self._token = {}
            """Le token obtenu via l'API pour utiliser les autres méthodes"""
            self._url = "https://api.partage.renater.fr/service/domain/"
            """L'url vers l'API BSS Partage"""
            self._ttl = 300

        @property
        def url(self):
            """Getter de l'url

               Arguments : Aucun

               Retour :
                    string : url de l'API BSS Partage

                Example d'utilisation :
                    >>>con = BSSConnexion("domain.com","6b7ead4bd425836e8cf0079cd6c1a05acc127acd07c8ee4b61023e19250e929c")
                    >>>url = con.url
                    >>>print(url)
                    https://api.partage.renater.fr/service/domain/
            """
            return self._url

        @url.setter
        def url(self,url):
            """Setter de l'url

            :param url:
                L'url vars l'api BSS par default https://api.partage.renater.fr/service/domaine
            """
            self._url = url

        @property
        def domain(self):
            """Getter du domaine

                Arguments : Aucun

                Retour :
                    string : domaine cible

                Example d'utilisation :
                    >>>con = BSSConnexion("domain.com","6b7ead4bd425836e8cf0079cd6c1a05acc127acd07c8ee4b61023e19250e929c")
                    >>>domain = con.domain
                    >>>print(domain)
                    domain.com
            """
            return self._domain

        @property
        def ttl(self):
            """
            Lecture de la durée de vie des tokens.

            :return: la durée de vie des tokens, en secondes.
            """
            return self._ttl

        @ttl.setter
        def ttl(self, value):
            self._ttl = value

        def setDomainKey(self, listDomainKey):
            """Getter du domaine

                :param listDomainKey: une liste conntenant l'emsemble des domaine à initialiser. Formate de la liste
                {"domaine1" : "keydomain1", "domaine2" : "keydomain2"}


                Example d'utilisation :
                    >>>con = BSSConnexion()
                    >>>con.setDomainKey({"domaine1" : "keydomain1", "domaine2" : "keydomain2"} )
            """
            if not isinstance(listDomainKey, dict):
                raise TypeError
            for domain in listDomainKey:
                if not utils.checkIsDomain(domain):
                    raise DomainException(domain + " n'est pas un nom de domain valide")
                self._key[domain] = listDomainKey[domain]
                self._timestampOfLastToken[domain] = 0
                self._token[domain] = ""

        def token(self, domain):
            """Getter du Token

                Arguments : Aucun

                Retour :
                    string : token pour connexion à l'API

                Exception:
                    BSSConnexion en cas d'Erreur lors de la récupération du token

                Example d'utilisation :
                    >>>con = BSSConnexion("domain.com","6b7ead4bd425836e8cf0079cd6c1a05acc127acd07c8ee4b61023e19250e929c")
                    >>>token = con.token
                    >>>try:
                    ... print(token) #doctest: +ELLIPSIS
                    ...except BSSConnexionException as err:
                    ... print("BSS Erreur: {0}".format(err))
                    ...
                Description :
                    Le token ayant une durée de vie de 5min on le regénère si il est plus vieux que 4min30s
                    Si l'ecart entre le timestamp actuel et le timestamp de l'obtention du dernier token est de moins de 270 secondes (4min30s)
                    on renvoie le token actuel. Au delà on génère un nouveau token
            """
            if isinstance(domain, str):
                if utils.checkIsDomain(domain):

                    self._domain = domain
                    """Le domaine sur lequel on souhaite travailler"""
                    if domain not in self._key:
                        raise DomainException(domain + " : Domaine non initialisé")
                    actualTimestamp = round(time())
                    if (actualTimestamp - self._timestampOfLastToken[domain]) < int( self._ttl * .9 ):
                        return self._token[domain]
                    else:
                        self._timestampOfLastToken[domain] = actualTimestamp
                        msg = domain + "|" + str(actualTimestamp)
                        preAuth = hmac.new(self._key[domain].encode("utf-8"), msg.encode("utf-8"), hashlib.sha1).hexdigest()
                        data = {
                            "domain": domain,
                            "timestamp": str(round(time())),
                            "preauth": preAuth
                        }
                        response = postBSS(self._url + "/Auth", data)
                        status_code = utils.changeToInt(response["status"])
                        message = response["message"]
                        if status_code == 0:
                            self._token[domain] = response["token"]
                        else:
                            raise BSSConnexionException(status_code, message)
                        return self._token[domain]
                else:
                    raise DomainException(domain+" n'est pas un nom de domain valide")
            else:
                raise TypeError

    instance = None

    def __new__(cls):  # _new_ est toujours une méthode de classe
        if not BSSConnexion.instance:
            BSSConnexion.instance = BSSConnexion.__BSSConnexion()
        return BSSConnexion.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)

