# -*-coding:utf-8 -*
class BSSConnexionException(Exception):
    """
    Exception levé lors d'une erreur de connexion

    :ivar message: message à afficher
    """
    def __init__(self,code, message):
        self.msg = str(code)+" : "+message