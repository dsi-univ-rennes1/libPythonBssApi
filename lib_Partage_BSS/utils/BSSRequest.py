# -*-coding:utf-8 -*
"""
Module permettant de faire des requêtes HTTP vers l'API BSS et de parser la réponse
"""
from lib_Partage_BSS.exceptions import TmpServiceException
import xml.etree.ElementTree as et
from xml.etree.ElementTree import ParseError
from xmljson import yahoo as ya
import requests,datetime,time

def parseResponse(stringXml):
    """
    Méthode permettant de transformer la reponse XML de l'API BSS en objet Python

    :param stringXml: la chaine XML à transformer en objet python
    :return: l'objet response obtenu
    """
    ts = time.time()
    dump_file = '/tmp/bss_incorrect_response.%s' % datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
    try:
        response = ya.data(et.fromstring(stringXml))
        if "Response" in response:
            return response["Response"]
        elif "response" in response:
            return response["response"]
        else:
            with open(dump_file, 'w') as dump:
                dump.write(stringXml)

            raise TmpServiceException.TmpServiceException(3,"Problème format réponse BSS ; réponse sauvegardée dans " + dump_file)

    except ParseError as e:
        with open(dump_file, 'w') as dump:
            dump.write(stringXml)

            raise TmpServiceException.TmpServiceException(3,"Problème format réponse BSS ; réponse sauvegardée dans " + dump_file + " : " + str(e)) from e


def postBSS(url, data):
    """
    Permet de récupérer la réponse d'une requête auprès de l'API BSS

    :param url: url de l'action demandée avec si nécessaire le token
    :param data: le body de la requête post
    :return: BSSResponse la réponse de l'API BSS
    """
    return parseResponse(requests.post(url, data=data).text)
