# -*-coding:utf-8 -*
"""
Module permettant de faire de requêtes HTTP vers l'API BSS et de parser la réponse
"""
import xml.etree.ElementTree as et
from xmljson import yahoo as ya
import requests


def parseResponse(stringXml):
    """
    Méthode permettant de transformer la reponse XML de l'API BSS en objet Python

    :param stringXml: la chaine XML à transformer en objet python
    :return: l'objet response obtenue
    """
    return ya.data(et.fromstring(stringXml))["Response"]

def postBSS(url, data):
    """
    Permet de récupérer la réponse d'une requête auprès de l'API BSS

    :param url: url de l'action demandé avec si nécessaire le token
    :param data: le body de la requête post
    :return: BSSResponse la reponse de l'API BSS
    """
    return parseResponse(requests.post(url, data).text)