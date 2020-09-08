# -*-coding:utf-8 -*
"""
Module général regroupant les méthodes communes des différents services
"""
import re
from lib_Partage_BSS import utils
from lib_Partage_BSS.services import BSSConnexion
from lib_Partage_BSS.utils.BSSRequest import postBSS
from lib_Partage_BSS.exceptions import NameException, DomainException, BSSConnexionException, ServiceException, TmpServiceException, NotFoundException


def extractDomain(mailAddress):
    """
    Méthode permettant d'extraire le domaine d'une adresse mail

    :param mailAddress: adresse mail pour extraire le domaine
    :return: le nom de domaine
    :raises NameException: Exception levée si l'adresse mail n'est pas valide
    """
    if utils.checkIsMailAddress(mailAddress):
        return mailAddress.split("@")[1]
    else:
        raise NameException("L'adresse mail " + mailAddress + " n'est pas valide")


def callMethod(domain, methodName, data):
    """
    Méthode permettant d'appeler une méthode de l'API BSS

    :param domain: le nom de domaine
    :param methodName: le nom de la méthode à appeler
    :param data: le body de la requête
    :return: la réponse reçue de l'API BSS
    :raises ServiceException: Exception levée si la requête vers l'API à echoué. L'exception contient le code de l'erreur et le message
    :raises DomainException: Exception levée si le domaine de l'adresse mail n'est pas un domaine valide
    """
    con = BSSConnexion()
    token = None
    try:
        token = con.token(domain)

    except BSSConnexionException as e:
        raise TmpServiceException(3, "Problème authentification BSS : " + str(e))

    except DomainException as e:
        raise ServiceException(3,"Problème authentification BSS : "+ str(e))

    return postBSS(con.url+"/"+methodName+"/"+token, data)

def checkResponseStatus(response):
    """
    Vérifie si le code status passé est un code de réussite ou pas (réussite = 0)
    Lève une exception selon le type d'erreur

    :param response: la réponse de l'appel à l'API
    :return: True si le code est 0, levée d'exception sinon
    :raises TypeError: Exception levée si le paramètre n'est pas un OrderedDict et si il ne possède pas un champs type avec la valeur integer
    """
    try:
        status = utils.changeToInt(response["status"])
    except TypeError:
        raise ServiceException(response["status"], response["message"])

    if status != 0:
        # On essaie de déterminer les erreurs temporaires versus définitives, à partir du contenu de response["message"]
        if re.search('(unable to get connection|Invalid token|Accès refusé|Une erreur système bloque votre requête|LDAP error|system failure|unable to create entry|unable to create account)', response["message"]):
            raise TmpServiceException(response["status"], response["message"])
        elif re.search('(no such account|no such domain|no such distribution list|no such cos)', response["message"]):
            raise NotFoundException(response["status"], response["message"])
        else:
            raise ServiceException(response["status"], response["message"])

    return True


