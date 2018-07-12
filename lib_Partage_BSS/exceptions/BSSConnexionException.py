# -*-coding:utf-8 -*
class BSSConnexionException(Exception):
    """
    Exception levée lors d'une erreur de connexion

    :ivar message: message à afficher
    """
    def __init__(self,code, message):
        self.msg = str(code)+" : "+str(message)