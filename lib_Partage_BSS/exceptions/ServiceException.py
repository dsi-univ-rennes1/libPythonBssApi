class ServiceException(Exception):

    def __init__(self,code, message):
        self.expr = "Erreur lors de l'appel de la methode"
        self.msg = str(code)+" : "+message