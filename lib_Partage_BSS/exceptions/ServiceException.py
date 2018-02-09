class ServiceException(Exception):

    def __init__(self, message):
        self.expr = "Erreur lors de l'appel de la methode"
        self.msg = message