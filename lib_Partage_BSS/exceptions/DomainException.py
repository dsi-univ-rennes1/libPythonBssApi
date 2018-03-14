# -*-coding:utf-8 -*
class DomainException(Exception):
    """
    Exception levée lors d'une erreur sur le nom de domaine

    :ivar message: message à afficher
    """
    def __init__(self, message):
        self.msg = message
