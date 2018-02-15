# -*-coding:Latin-1 -*

import requests

from lib_Partage_BSS.utils.ParseBSSResponse import parseResponse


def postBSS(url, data):
    """
    Permet de récupérer la réponse d'une requête auprès de l'API BSS
    :param url: url de l'action demandé avec si nécessaire le token
    :param data: le body de la requête post
    :return: BSSResponse la reponse de l'API BSS
    """

    return parseResponse(requests.post(url, data).text)
