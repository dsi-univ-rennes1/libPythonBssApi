from lib_Partage_BSS import utils
from lib_Partage_BSS.services import BSSConnexion
from lib_Partage_BSS.utils.PostBSSApi import postBSS


def extractDomain(mailAddress):
    if utils.checkIsMailAddress(mailAddress):
        return mailAddress.split("@")[1]
    else:
        raise TypeError


def callMethod(domain, methodName, data):
    con = BSSConnexion()
    return postBSS(con.url+"/"+methodName+"/"+con.token(domain), data)



