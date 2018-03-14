# -*-coding:utf-8 -*
"""
Module contenant les méthodes de vérification de paramètres et de conversion de paramètres
"""
import re
from collections import OrderedDict
from datetime import datetime
from time import mktime

from lib_Partage_BSS.exceptions import NameException


def checkIsNum(value):
    """
    Vérifie si la valeur passée en paramètre est un nombre

    :param value: la valeur a tester
    :return: True si c'est un nombre False sinon
    :raises TypeError: Exception levée si le paramètre n'est pas un str
    """
    if isinstance(value, str):
        if value == "" or re.match("^[0-9 .\-_/]*$", value):
            return True
        else:
            return False
    else:
        raise TypeError


def checkIsMailAddress(value):
    """
    Vérifie si la valeur passée en paramètre est une adresse mail

    :param value: la valeur à tester
    :return: True si c'est une adresse mail ou vide False sinon
    :raises TypeError: Exception levée si le paramètre n'est pas un str
    """
    if isinstance(value, str):
        if value == "" or re.match("^[^\W][a-zA-Z0-9_\-]*(\.[a-zA-Z0-9_\-]+)*\@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*\.[a-zA-Z]{2,4}$", value):
            return True
        else:
            return False
    else:
        raise TypeError


def checkIsDomain(value):
    """
    Vérifie si la valeur passée en paramètre est un nom de domaine

    :param value: la valeur a tester
    :return: True si c'est un domain False sinon
    :raises TypeError: Exception levée si le paramètre n'est pas un str
    """
    if isinstance(value, str):
        if value == "" or re.match("^[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*\.[a-zA-Z]{2,4}$", value):
            return True
        else:
            return False
    else:
        raise TypeError


def checkIsPreDeleteAccount(value):
    """
    Vérifie si la valeur passée en paramètre est un nom de compte en pré instance de suppression (deleted_timestamp_nom)

    :param value: l'identifiant du compte
    :return: True si c'est un compte en instance de suppression False sinon
    :raises TypeError: Exception levée si le paramètre n'est pas un str
    """
    if isinstance(value, str):
            if re.match("^readytodelete_\d{4}[\-]\d{2}[\-]\d{2}[\-]\d{2}[\-]\d{2}[\-]\d{2}_.*", value):
                if checkIsMailAddress(value.split("_")[2]):
                    return True
                else:
                    return False
            else:
                return False
    else:
        raise TypeError


def checkResponseStatus(statuscode):
    """
    Vérifie si le code status passé est un code de réussite ou pas (réussite = 0)

    :param statuscode: le code status à tester
    :return: True si le code est 0 False sinon
    :raises TypeError: Exception levée si le paramètre n'est pas un OrderedDict et si il ne possède pas un champs type avec la valeur integer
    """
    try:
        return changeToInt(statuscode) == 0
    except TypeError:
        return False


def changeBooleanToString(boolean):
    """
    Permet de changer les booleen True et False en String.

    :param booleanString: le booléen à changer en String
    :return: "TRUE" ou  "FALSE"
    :raises TypeError: Exception levée si le paramètre n'est pas un bool
    """
    if boolean is not None:
        if isinstance(boolean, bool):
            if boolean:
                return "TRUE"
            else:
                return "FALSE"
        else:
            raise TypeError()
    else:
        return None


def changeStringToBoolean(booleanString):
    """
    Permet de changer les chaînes TRUE et FALSE (quelque soit leurs casse) en booléen.
    Renvoie un TypeErreur sinon

    :param booleanString: "TRUE" ou  "FALSE"
    :return: renvoie le booleen correspondant
    :raises TypeError: Exception levée si le paramètre n'est pas un String
    """
    if booleanString is not None:
        if isinstance(booleanString, str):
            if booleanString.upper() == "TRUE":
                return True
            elif booleanString.upper() == "FALSE":
                return False
            else:
                return None
        else:
            raise TypeError()
    else:
        return None


def changeToInt(value):
    """
    Permet de changer les réponses qui contiennent le type integer en int

    :param value: la valeur de la réponse à changer en int
    :return: renvoie le int correspondant
    :raises TypeError: Exception levée si le paramètre n'est pas un OrderedDict et si il ne possède pas un champs type avec la valeur integer
    """
    if value is not None:
        if isinstance(value, OrderedDict):
            if value["type"] == "integer":
                return int(value["content"])
            else:
                raise TypeError
        else:
            raise TypeError
    else:
        return None


def changeTimestampToDate(timestamp):
    """
    Méthode permettant de changer un timestamp en date de forme AAAA-MM-JJ-HH-MM-SS

    :param timestamp: le timestamp à convertir
    :return: la date obtenue
    :raises TypeError: Exception levée si le paramètre n'est pas un integer
    """
    if isinstance(timestamp, int):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d-%H-%M-%S')
    else:
        raise TypeError


def changeDateToTimestamp(strDate):
    """
    éthode permetant de changer un string date de forme AAAA-MM-JJ-HH-MM-SS en timestamp
    :param date: la date à convertir
    :return: le timestamp obtenue
    :raises TypeError: Exception levée si le paramètre n'est pas un String
    """
    if isinstance(strDate, str):
        return mktime(datetime.strptime(strDate, '%Y-%m-%d-%H-%M-%S').timetuple())
    else:
        raise TypeError
