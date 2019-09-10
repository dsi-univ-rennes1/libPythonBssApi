# -*-coding:utf-8 -*
"""
Module contenant les méthodes permettant d'appeler les services de l'API BSS concernant les classes de service
"""
import re
from collections import OrderedDict
from time import time

from lib_Partage_BSS import models, utils, services
from lib_Partage_BSS.exceptions import NameException, DomainException, ServiceException, TmpServiceException, NotFoundException
from .GlobalService import callMethod, checkResponseStatus


def fillCOS(cosResponse):
    """
    Permet de remplir un objet COS depuis une réponse de l'API BSS

    :param cosResponse: l'objet COS renvoyé par l'API
    :return: l'objet COS créé
    :raises ServiceException: Exception levée si la requête vers l'API à echoué. L'exception contient le code de l'erreur et le message
    :raises NameException: Exception levée si le nom n'est pas une adresse mail valide
    """

    retCOS = models.COS(cosResponse["name"])
    cosKeys = cosResponse.keys()
    for attr in cosKeys:
        if cosResponse[attr] is not None:
            if isinstance(cosResponse[attr], str):
                if cosResponse[attr] == "TRUE" or cosResponse[attr] == "FALSE":
                    retCOS.__setattr__(attr, utils.changeStringToBoolean(cosResponse[attr]))
                else:
                    retCOS.__setattr__(attr, cosResponse[attr])
            elif isinstance(cosResponse[attr], OrderedDict):
                if "type" in cosResponse[attr].keys():
                    if cosResponse[attr]["type"] == "integer":
                        retCOS.__setattr__(attr, int(cosResponse[attr]["content"]))
                    elif cosResponse[attr]["type"] == "array":
                        if attr == "zimbraZimletAvailableZimlets":
                            retCOS.__setattr__(attr, cosResponse[attr]["zimbraZimletAvailableZimlet"])
                        elif attr == "zimbraMailAlias":
                            retCOS.__setattr__(attr, cosResponse[attr]["zimbraMailAlias"])
    return retCOS


def getCOS(domain, name):
    """
    Méthode permettant de récupérer les informations d'une classe de service via l'API BSS

    :return: La classe de service récupérée ou None si la classe de service n'existe pas
    :raises ServiceException: Exception levée si la requête vers l'API à echoué. L'exception contient le code de l'erreur et le message
    :raises NameException: Exception levée si le nom n'est pas une adresse mail valide
    :raises DomainException: Exception levée si le domaine de l'adresse mail n'est pas un domaine valide
    """

    data = {
        "name": name
    }
    response = callMethod(domain, "GetCos", data)

    try:
        checkResponseStatus(response)
    except NotFoundException:
        return None

    cos = response["cos"]
    return fillCOS(cos)


def getAllCOS(domain):
    """
    Permet de rechercher toutes les classes de service d'un domain

    :param domain: le domaine de la recherche
    :raises ServiceException: Exception levée si la requête vers l'API à echoué. L'exception contient le code de l'erreur et le message
    :raises DomainException: Exception levée si le domaine n'est pas un domaine valide
    """
    if not utils.checkIsDomain(domain):
        raise DomainException(domain + " n'est pas un nom de domain valide")
    response = callMethod(domain, "GetAllCos", { } )
    checkResponseStatus(response)
    if len(response["coses"]) == 1:
        return []
    else:
        coses = response["coses"]["cose"]
        retCoses = []
        if isinstance(coses, list):
            for cos in coses:
                retCoses.append(fillCOS(cos))
        else:
            retCoses.append(fillCOS(coses))
        return retCoses

