from collections import OrderedDict

import pytest

from lib_Partage_BSS.utils import checkIsNum, checkIsMailAddress, checkIsDomain, checkIsPreDeleteAccount, \
    changeBooleanToString, changeStringToBoolean, changeToInt, changeTimestampToDate, \
    changeDateToTimestamp


def test_checkIsNum_casTrueSansSeparateur():
    assert checkIsNum("0123456789")


def test_checkIsNum_casTrueAvecTiret():
    assert checkIsNum("01-23-45-67-89")


def test_checkIsNum_casTrueAvecPoint():
    assert checkIsNum("01.23.45.67.89")


def test_checkIsNum_casTrueAvecEspace():
    assert checkIsNum("01 23 45 67 89")

def test_checkIsNum_casTrueAvecUnderscore():
    assert checkIsNum("01_23_45_67_89")


def test_checkIsNum_casTrueAvecSlash():
    assert checkIsNum("01/23/45/67/89")


def test_checkIsNum_casTrueVide():
    assert checkIsNum("")


def test_checkIsNum_casFalseAvecLettre():
    assert not checkIsNum("01/23/45/67/89a")


def test_checkIsNum_casFalseAvecCaractereSpecial():
    assert not checkIsNum("01/23/45/67/89{")


def test_checkIsMailAddress_casTrueAvecDebutEn1Partie():
    assert checkIsMailAddress("test@domain.com")


def test_checkIsMailAddress_casTrueAvecDebutEn2Parties():
    assert checkIsMailAddress("super.test@domain.com")


def test_checkIsMailAddress_casTrueAvecApostrophe():
    assert checkIsMailAddress("super'test@domain.com")


def test_checkIsMailAddress_casTrueAvecPlus():
    assert checkIsMailAddress("super+test@domain.com")


def test_checkIsMailAddress_casTrueVide():
    assert checkIsMailAddress("")


def test_checkIsMailAddress_casFalseSansDomain():
    assert not checkIsMailAddress("super.test")


def test_checkIsMailAddress_casFalseSansExtensionDeDomain():
    assert not checkIsMailAddress("super.test@domain")


def test_checkIsMailAddress_casFalseSansAdresseMaisAvecDomaine():
    assert not checkIsMailAddress("@domain.fr")


def test_checkIsDomain_casTrueDomainAvecExtension2caracteres():
    assert checkIsDomain("domain.fr")


def test_checkIsDomain_casTrueDomainAvecExtension4caracteres():
    assert checkIsDomain("domain.fran")


def test_checkIsDomain_casTrueDomainAvecSousDomaine():
    assert checkIsDomain("test.domain.fr")


def test_checkIsDomain_casFalseDomainAvecExtension5caracteres():
    assert not checkIsDomain("domain.franc")


def test_checkIsDomain_casFalseDomainAvecExtension1caractere():
    assert not checkIsDomain("domain.f")


def test_checkIsPreDeleteAccount_casTrue():
    assert checkIsPreDeleteAccount("readytodelete_2018-03-09-12-00-00_test@domain.fr")


def test_checkIsPreDeleteAccount_casFalsePasreadytodeleteAuDebut():
    assert not checkIsPreDeleteAccount("readytodelet_2018-03-09-12-00-00_test@domain.fr")


def test_checkIsPreDeleteAccount_casFalseMauvaisFormatDate():
    assert not checkIsPreDeleteAccount("readytodelete_2018/03/09/12:00:00_test@domain.fr")


def test_checkIsPreDeleteAccount_casFalseDateIncomplete():
    assert not checkIsPreDeleteAccount("readytodelete_2018-03-09-12-00_test@domain.fr")


def test_checkIsPreDeleteAccount_casFalsePasAdresseMailALaFin():
    assert not checkIsPreDeleteAccount("readytodelete_2018-03-09-12-00_test")

def test_changeBooleanToString_casTrueParamTrue():
    assert changeBooleanToString(True) == "TRUE"


def test_changeBooleanToString_casTrueParamFalse():
    assert changeBooleanToString(False) == "FALSE"


def test_changeStringToBoolean_casTrueParamTRUE():
    assert changeStringToBoolean("TRUE")


def test_changeStringToBoolean_casTrueParamFALSE():
    assert not changeStringToBoolean("FALSE")


def test_changeStringToBoolean_casNoneParamAUTRE():
    assert changeStringToBoolean("AUTRE") is None


def test_changeToInt_casTrueInteger():
    test_int = OrderedDict()
    test_int["type"] = "integer"
    test_int["content"] = "1"
    assert isinstance(changeToInt(test_int), int)


def test_changeToInt_casException():
    with pytest.raises(TypeError):
        test_int = OrderedDict()
        test_int["type"] = "string"
        test_int["content"] = "1"
        changeToInt(test_int)


def test_changeTimestampToDate_casOk():
    assert changeTimestampToDate(1520512483) == "2018-03-08-13-34-43"


def test_changeDateToTimestamp_casOk():
    assert changeDateToTimestamp("2018-03-08-13-34-43") == 1520512483