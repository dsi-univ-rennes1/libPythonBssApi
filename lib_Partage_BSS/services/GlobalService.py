# -*-coding:utf-8 -*
"""
Module générale regroupant les méthodes communes des différents services
"""
from lib_Partage_BSS import utils
from lib_Partage_BSS.exceptions import NameException
from lib_Partage_BSS.services import BSSConnexion
from lib_Partage_BSS.utils.BSSRequest import postBSS


def extractDomain(mailAddress):
    """
    Méthode permettant d'extraire le domaine d'une adresse mail

    :param mailAddress: adresse mail pour extraire le domaine
    :return: le nom de domaine
    :raises NameException: Exception levé si l'adresse mail n'est pas valide
    """
    if utils.checkIsMailAddress(mailAddress):
        return mailAddress.split("@")[1]
    else:
        raise NameException("L'adresse mail " + mailAddress + " n'est pas valide")


def callMethod(domain, methodName, data):
    """
    Méthode permettant d'appeller une méthode de l'API BSS

    :param domain: le nom de domaine
    :param methodName: le nom de la méthode à appeller
    :param data: le body de la requête
    :return: la réponse reçu de l'API BSS
    :raises ServiceException: Exception levé si la requête vers l'API à echoué. L'exception contient le code de l'erreur et le message
    :raises DomainException: Exception levé si le domaine de l'adresse mail n'est pas un domaine valide
    """
    con = BSSConnexion()
    return postBSS(con.url+"/"+methodName+"/"+con.token(domain), data)



