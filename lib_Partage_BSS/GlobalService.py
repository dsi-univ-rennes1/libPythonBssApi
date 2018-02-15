# -*-coding:Latin-1 -*

from lib_Partage_BSS.utils.PostBSSApi import postBSS


class GlobalService:

    def __init__(self, connexion, name):
        self._con = connexion
        self._name = name

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def callMethod(self, methodName, data):
        return postBSS(self._con.url+"/"+methodName+"/"+self._con.token, data)

    def showAttr(self):
        ret = ""
        for key in self.__dict__.keys():
            if self.__dict__[key] is not None:
                ret += (key+" : "+str(self.__dict__[key])+"\n")
        return ret
