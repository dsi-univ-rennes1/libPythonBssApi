# -*-coding:utf-8 -*
class GlobalModel:
    """
    Classe générale regroupant les méthodes communes des différents model
    """
    def __init__(self, name):
        self._name = name

    def showAttr(self):
        """
        Méthode permettant d'avoir un string listant tout les attribut non null du model

        :return: string contenant la liste des attributs du model
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

        :return: le nom du model
        """
        return self._name

    def setName(self, newValue):
        """
        Setter de name

        :param newValue: le nouveau nom du model
        """
        self._name = newValue