class ParseException(Exception):

    def __init__(self, message):
        self.expr = "Erreur lors du parsage de l'attribut"
        self.msg = message
