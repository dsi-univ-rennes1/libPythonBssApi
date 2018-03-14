# -*-coding:utf-8 -*
class GlobalModel:
    """
    Classe générale regroupant les méthodes communes des différents modèles
    """
    def __init__(self, name):
        self._name = name

    def showAttr(self):
        """
        Méthode permettant d'avoir un string listant tous les attributs non null du modèle

        :return: string contenant la liste des attributs du modèle
        """
        ret = ""
        for key in self.__dict__.keys():
            if self.__dict__[key] is not None:
                ret += (key+" : "+str(self.__dict__[key])+"\n")
        return ret

    @property
    def getName(self):
        """
        Getter de name

        :return: le nom du modèle
        """
        return self._name

    def setName(self, newValue):
        """
        Setter de name

        :param newValue: le nouveau nom du modèle
        """
        self._name = newValue