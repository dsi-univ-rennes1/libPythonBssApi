import re
from collections import OrderedDict


def checkIsNum(value):
    """
    Vérifie si la valeur passé en paramètre est un numéro ou pas (constitué uniquement de digit)
    :param value: la valeur a tester
    :return: True si c'est un numéro False sinon
    """
    return re.match("^[0-9 .\-_/]*$", value)


def checkIsMailAddress(value):
    """
    Vérifie si la valeur passé en paramètre est une adresse mail ou pas (contient une chaine suivi d'un @ suivi d'une chaine suivi d'un point suivi d'une chaine)
    :param value: la valeur a tester
    :return: True si c'est une adresse mail False sinon
    """
    return re.match("^[^\W][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)*\@[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\.[a-zA-Z]{2,4}$", value)


def checkIsDomain(value):
    return re.match("^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\.[a-zA-Z]{2,4}$", value)


def checkResponseStatus(statuscode):
    return changeToInt(statuscode) == 0


def changeBooleanToString(boolean):
    """
    Permet de changer les booleen True et False en String correspondant entièrement en majuscule.
    :param booleanString: le booleen à changer en String
    :return: "TRUE" ou  "FALSE"
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
    Permet de changer les chaines TRUE et FALSE (quelque soit leurs case) en booleen correspondant.
    Renvoie un TypeErreur sinon
    :param booleanString: "TRUE" ou  "FALSE"
    :return: renvoie le booleen correspondant
    """
    if booleanString is not None:
        if isinstance(booleanString, str):
            if booleanString.upper() == "TRUE":
                return True
            elif booleanString.upper() == "FALSE":
                return False
        else:
            raise TypeError()
    else:
        return None


def changeToInt(value):
    if value is not None:
        if isinstance(value, OrderedDict):
            if value["type"] == "integer":
                return int(value["content"])
        else:
            raise TypeError
    else:
        return None
