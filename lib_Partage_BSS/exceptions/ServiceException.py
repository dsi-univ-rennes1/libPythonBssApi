# -*-coding:utf-8 -*
from lib_Partage_BSS import utils
class ServiceException(Exception):
    """
    Exception levée lorsqu'un appel à l'API échoue

    :ivar code: code de l'erreur
    :ivar message: message à afficher
    """
    def __init__(self,code, message):
        self.code = utils.changeToInt(code)
        self.msg = str(utils.changeToInt(code))+" : "+message
