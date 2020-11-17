# -*-coding:utf-8 -*
"""
Module contenant les méthodes permettant d'appeler les services de l'API BSS concernant les partages
"""

from lib_Partage_BSS import models, utils, services
from lib_Partage_BSS.exceptions import NameException, DomainException, ServiceException, TmpServiceException, NotFoundException
from .GlobalService import callMethod, checkResponseStatus

#-------------------------------------------------------------------------------


def addRootShare(account,recipients=[],rights=["sendAs"]):
    """
    Ajoute les droits de partage sur une boite fonctionnelle

    :param account: le nom de la boite (adresse mail).
    :param recipients: un tableau contenant les adresses des comptes à qui autoriser le partage.
    :param rights: Les droit donnés pour l'envoi de mail:\
        sendAs="en tant que", sendOnBehalfOf="de la part de"

    :raises TypeError: si la liste recipients est vide
    :raises NameError: si l'adresse du partage à créer est invalide
    """
    data = {}
    
    # Si la liste est vide
    if not(recipients):
        raise TypeError

    # On vérifie si le mail est valide
    if not utils.checkIsMailAddress( account ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( account ) )
    else :
        # Préparation des attributs 
        data.update({
                "account": account,
                "recipients[]": recipients,
                "rights[]": rights
            })
        
        response = callMethod(services.extractDomain(account), "/account/AddRootShare", data)
        checkResponseStatus(response)

#-------------------------------------------------------------------------------


def RemoveRecipientsFromRootShare(account,recipients=[]):
    """
    Retire les droits de partage sur une boite fonctionnelle 

    :param account: le nom de la boite (adresse mail).
    :param recipients: un tableau contenant les adresses des comptes à qui supprimer le partage.

    :raises TypeError: si la liste recipients est vide
    :raises NameError: si l'adresse du partage à créer est invalide
    """
    data = {}
    
    # Si la liste est vide
    if not(recipients):
        raise TypeError

    # On vérifie si le mail est valide
    if not utils.checkIsMailAddress( account ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( account ) )
    else :
        # Préparation des attributs 
        data.update({
                "account": account,
                "recipients[]": recipients
            })

        response = callMethod(services.extractDomain(account), "/account/RemoveRecipientsFromRootShare", data)
        checkResponseStatus(response)

#-------------------------------------------------------------------------------

def RemoveRootShare(account):
    """
    Cet appel permet de retirer un partage root d'une boites de service d'un ou plusieurs utilisateurs

    :param account: Adresse email du compte qui fournit le partage root
    :raises NameError: si l'adresse du partage à créer est invalide
    """
    data = {}
    # On vérifie si le mail est valide
    if not utils.checkIsMailAddress( account ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( account ) )
    else :
        # Préparation des attributs 
        data.update({
                "account": account,
            })

        response = callMethod(services.extractDomain(account), "/account/RemoveRootShare", data)
        checkResponseStatus(response)

#-------------------------------------------------------------------------------

def AddRootDelegate(account,right=["sendAs"]):
    """
    Cet appel permet d'ajouter aux bénéficiaires d'un partage root le droit d'envoyer des email \
    "en tant que" et/ou "de la part de" de la boite de service source.

    :param account: Adresse email du compte qui fournit le partage root
    :param rights: Les droit donnés pour l'envoi de mail:\
        sendAs="en tant que", sendOnBehalfOf="de la part de"

    :raises NameError: si l'adresse du partage à créer est invalide
    """
    data = {}
    # On vérifie si le mail est valide
    if not utils.checkIsMailAddress( account ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( account ) )
    else :
        # Préparation des attributs 
        data.update({
                "account": account,
                "right": right
            })

        response = callMethod(services.extractDomain(account), "/account/AddRootDelegate", data)
        checkResponseStatus(response)

def RemoveRootDelegate(account,right=["sendAs"]):
    """
    Cet appel permet de retirer aux bénéficiaires d'un partage root le droit d'envoyer des email \
    "en tant que" et/ou "de la part de" de la boite de service source.

    :param account: Adresse email du compte qui fournit le partage root
    :param rights: Les droit retirés pour l'envoi de mail:\
        sendAs="en tant que", sendOnBehalfOf="de la part de"

    :raises NameError: si l'adresse du partage à créer est invalide
    """
    data = {}
    # On vérifie si le mail est valide
    if not utils.checkIsMailAddress( account ):
        raise NameException( "L'adresse mail {} n'est pas valide".format( account ) )
    else :
        # Préparation des attributs 
        data.update({
                "account": account,
                "right": right
            })

        response = callMethod(services.extractDomain(account), "/account/RemoveRootDelegate", data)
        checkResponseStatus(response)
