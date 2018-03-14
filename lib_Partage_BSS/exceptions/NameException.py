# -*-coding:utf-8 -*
class NameException(Exception):
    """
    Exception levée lorsqu'un nom d'objet n'est pas conforme

    :ivar message: message à afficher
    """
    def __init__(self, message):
        self.msg = message
