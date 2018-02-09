class NameException(Exception):

    def __init__(self, message):
        self.expr = "Erreur de nom"
        self.msg = message
