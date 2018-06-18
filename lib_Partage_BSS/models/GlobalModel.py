# -*-coding:utf-8 -*
import json


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

    def __repr__( self ):
        """
        Transforme les données du compte en une chaîne pouvant être utilisée
        pour le débogage.
        """
        return '{}({})'.format( self.__class__.__name__ , ','.join( [
                '{}={}'.format( k , repr( v ) )
                    for k,v in self.__dict__.items( )
                        if v is not None
            ] ) )

    @property
    def name(self):
        """
        Getter de name

        :return: le nom du modèle
        """
        return self._name

    @name.setter
    def name(self, newValue):
        """
        Setter de name

        :param newValue: le nouveau nom du modèle
        """
        self._name = newValue

    def exportJsonAccount(self):
        json_data = {}
        for key in self.__dict__.keys():
            json_data[key[1:]]= self.__dict__[key]
        with open(self._name+".json", "w") as json_file:
            json_file.write(json.dumps(json_data, indent=4))





