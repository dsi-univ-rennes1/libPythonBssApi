class DomainException(Exception):

    def __init__(self):
        self.expr = "Erreur domaine"
        self.msg = "Domaine non présent dans le fichier de config config_lib_bss.json"
