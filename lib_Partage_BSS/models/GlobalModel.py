from lib_Partage_BSS import utils
import re

class GlobalModel:

    def __init__(self, name):
        self._name = name

    def showAttr(self):
        ret = ""
        for key in self.__dict__.keys():
            if self.__dict__[key] is not None:
                ret += (key+" : "+str(self.__dict__[key])+"\n")
        return ret

    @property
    def getName(self):
        return self._name

    def setName(self, newValue):
        self._name = newValue