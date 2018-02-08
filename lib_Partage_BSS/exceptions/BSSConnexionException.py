# -*-coding:Latin-1 -*
class BSSConnexionException(Exception):
    """
    Exception levé lors d'une erreur de connexion
    """
    def __init__(self, message):
        self.expr = "Erreur de connection"
        self.msg = message