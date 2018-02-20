from collections import OrderedDict

from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS import models, utils, services
from .GlobalService import callMethod


def getAccount(name):
    """
    Méthide permettant de récuperer les informations d'un compte via l'API BSS
    :return: Le compte récupéré
    """
    retAccount = models.Account(name)
    data = {
        "name": name
    }

    response = callMethod(services.extractDomain(name), "GetAccount", data)
    if utils.checkResponseStatus(response["status"]):
        account = response["account"]
        accountKeys = account.keys()
        for attr in accountKeys:
            if account[attr] is not None:
                if isinstance(account[attr], str):
                    if account[attr] == "TRUE" or account[attr] == "FALSE":
                        retAccount.__setattr__("_"+attr,utils.changeStringToBoolean(account[attr]))
                    else:
                        retAccount.__setattr__("_" + attr, account[attr])
                elif isinstance(account[attr], OrderedDict):
                    if "type" in account[attr].keys():
                        if account[attr]["type"] == "integer":
                            retAccount.__setattr__("_" + attr, int(account[attr]["content"]))
                        elif account[attr]["type"] == "array":
                            if attr == "zimbraZimletAvailableZimlets":
                                retAccount.__setattr__("_" + attr, account[attr]["zimbraZimletAvailableZimlet"])
                            elif attr == "zimbraMailAlias":
                                retAccount.__setattr__("_" + attr, account[attr]["zimbraMailAlias"])
        return retAccount
    else:
        raise ServiceException(response["status"], response["message"])


def createAccount(name,userPassword, cosId):
    """
    Méthode permettant de créer un compte via l'API BSS en lui passant en paramètre l'empreinte du mot de passe (SSHA) et le cosId
    :param userPassword: le mot de passe de l'utilisateur hashé en SSHA1
    :param cosId: l'identifiant du cosId à appliquer pour le compte
    :return:
    """
    if userPassword[:6] == "{ssha}":
        data = {
            "name": name,
            "password": "",
            "userPassword": userPassword,
            "zimbraHideInGal": "FALSE",
            "zimbraCOSId": cosId
        }
        response = callMethod(services.extractDomain(name), "CreateAccount", data)
        if utils.checkResponseStatus(response["status"]):
            return getAccount(name)
        else:
            raise ServiceException(response["status"], response["message"])


def deleteAccount(name):
    data = {
        "name": name
    }
    response = callMethod(services.extractDomain(name), "DeleteAccount", data)
    if not utils.checkResponseStatus(response["status"]):
        raise ServiceException(response["status"], response["message"])


def modifyAccount(account):
    data = {}
    for attr in account.__dict__:
        if attr != "_zimbraZimletAvailableZimlets":
            if account.__getattribute__(attr) is not None:
                attrValue = account.__getattribute__(attr)
                if isinstance(attrValue, bool):
                    attrValue = utils.changeBooleanToString(attrValue)
                data[attr[1:]] = attrValue
    response = callMethod(services.extractDomain(account.getName), "ModifyAccount", data)
    if not utils.checkResponseStatus(response["status"]):
        raise ServiceException(response["status"], response["message"])


def modifyPassword(name, newUserPassword):
    """
    Pour modifier le mot de passe on n'accept que l'emprunte du mot de passe.
    On commence par faire un SetPassword avec une valeur factise pour forcer la déconnection des session en cours
    On passe ensuite via ModifyAccount l'empreinte du nouveau mot de passe
    :param newUserPassword:
    :return:
    """
    data={
        "name": name,
        "password": "valeurPourDeconnecterLesSessions"
    }
    response = callMethod(services.extractDomain(name), "SetPassword", data)
    if not utils.checkResponseStatus(response["status"]):
        raise ServiceException(response["status"], response["message"])
    data = {
        "name": name,
        "userPassword": newUserPassword
    }
    response = callMethod(services.extractDomain(name), "ModifyAccount", data)
    if not utils.checkResponseStatus(response["status"]):
        raise ServiceException(response["status"], response["message"])


def addAccountAlias(name, newAlias):
    data = {
        "name": name,
        "alias": newAlias
    }
    response = callMethod(services.extractDomain(name), "AddAccountAlias", data)
    if not utils.checkResponseStatus(response["status"]):
        raise ServiceException(response["status"], response["message"])


def removeAccountAlias(name, aliasToDelete):
    data = {
        "name": name,
        "alias": aliasToDelete
    }
    response = callMethod(services.extractDomain(name), "RemoveAccountAlias", data)
    if not utils.checkResponseStatus(response["status"]):
        raise ServiceException(response["status"], response["message"])


def modifyAccountAliases(name, listOfAliases):
    if isinstance(listOfAliases, list):

        account = getAccount(name)
        for alias in listOfAliases:
            if isinstance(account.getZimbraMailAlias(), list) or isinstance(account.getZimbraMailAlias(), str):
                if alias not in account.getZimbraMailAlias():
                    addAccountAlias(name, alias)
            elif account.getZimbraMailAlias() is None:
                addAccountAlias(name, alias)
        if isinstance(account.getZimbraMailAlias(), list):
            for alias in account.getZimbraMailAlias():
                if alias not in listOfAliases:
                    removeAccountAlias(name, alias)
        elif isinstance(account.getZimbraMailAlias(), str):
            if account.getZimbraMailAlias() not in listOfAliases:
                removeAccountAlias(name, account.getZimbraMailAlias())