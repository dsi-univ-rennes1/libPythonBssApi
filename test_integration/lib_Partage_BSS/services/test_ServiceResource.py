import pytest
from lib_Partage_BSS.models import  Resource
from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS.exceptions.NotFoundException import NotFoundException
from lib_Partage_BSS.services import AccountService, BSSConnexion, ResourceService
import time as timer

def create_account(name):
    account = AccountService.getAccount(name)
    if account == None:
        AccountService.createAccount(name,"{ssha}BIDON")

def delete_resource(name):
    resource = ResourceService.getResource(name)
    if resource != None:
        ResourceService.deleteResource(name)

def test_cleanup_bss_environment(test_config):
    print("Cleanup BSS environment before running tests...")
    #create_account(test_config['accountname'])
    delete_resource(test_config['resourcename'])

def test_createResource_cas_normal(test_config):
    newResource = ResourceService.createResource(test_config['resourcename'],test_config['displayName'],test_config['userPassword'],test_config['zimbraCalResType'],password=None)
    resource = ResourceService.getResource(test_config['resourcename'])
    assert resource.name == test_config['resourcename']


def test_createResource_cas_resourceExistant(test_config):
    with pytest.raises(ServiceException):
        newGroup = ResourceService.createResource(test_config['resourcename'],test_config['displayName'],test_config['userPassword'],test_config['zimbraCalResType'],password=None)

def test_getResource_cas_normal(test_config):
    resource = ResourceService.getResource(test_config['resourcename'])
    assert resource.name == test_config['resourcename']

def test_getResource_cas_resource_inexistant(test_config):
    with pytest.raises(ServiceException) as excinfo:
        resource = ResourceService.getResource("inexistant" + '@' + test_config['bss_domain'])

def test_modifyResource_cas_Normal(test_config):
    resource_as_dict = {'co': "France",
                        'description': "description de la ressource",
                        'displayName': "TestName",
                        'l': "Rennes",
                        'postalCode': "00000555",
                        'st': "état ressource",
                        'street': "la rue",
                        'zimbraAccountStatus': 'closed',
                        'zimbraCalResAutoAcceptDecline': "FALSE",
                        'zimbraCalResAutoDeclineIfBusy': "FALSE",
                        'zimbraCalResAutoDeclineRecurring': "FALSE",
                        'zimbraCalResBuilding': "le bâtiment",
                        'zimbraCalResCapacity': "12",
                        'zimbraCalResContactEmail': "qulqun@univ-x.fr",
                        'zimbraCalResContactName': "Quelqu'un",
                        'zimbraCalResContactPhone': "02567",
                        'zimbraCalResFloor': "sous-sol",
                        'zimbraCalResLocationDisplayName': "nom affiché",
                        'zimbraCalResRoom': "salle 17",
                        'zimbraCalResSite': "mon campus",
                        'zimbraCalResType': "Location",
                        'zimbraNotes': "notes non affichées",
                        }
    resource = ResourceService.getResource(test_config['resourcename'])
    for attribute in resource_as_dict:
        setattr(resource, "_" + attribute, resource_as_dict[attribute])
    ResourceService.modifyResource(resource)
    resource = ResourceService.getResource(test_config['resourcename'])
    errors = 0
    for attribute in resource_as_dict:
        if getattr(resource, "_" + attribute) != resource_as_dict[attribute]:
            errors = errors + 1
            print("Attribute '%s' does not match: '%s' vs '%s'" % (attribute, getattr(resource, "_" + attribute), resource_as_dict[attribute]))
    assert errors == 0

def test_modifyResource_cas_addZimbraPrefCalendarForwardInvitesTo(test_config):
    resource = ResourceService.getResource(test_config['resourcename'])
    resource.addZimbraPrefCalendarForwardInvitesTo("resource@x.fr")
    ResourceService.modifyResource(resource)
    resource = ResourceService.getResource(test_config['resourcename'])

    assert "resource@x.fr" in resource.zimbraPrefCalendarForwardInvitesTo

def test_modifyResource_cas_addZimbraPrefCalendarForwardInvitesToCompteErrone(test_config):
    resource = ResourceService.getResource(test_config['resourcename'])
    with pytest.raises(TypeError) as excinfo:
        resource.addZimbraPrefCalendarForwardInvitesTo("resourcettx.fr")
    
def test_modifyResource_cas_removeZimbraPrefCalendarForwardInvitesTo(test_config):
    resource = ResourceService.getResource(test_config['resourcename'])
    resource.removeZimbraPrefCalendarForwardInvitesTo("resource@x.fr")
    ResourceService.modifyResource(resource)
    resource1 = ResourceService.getResource(test_config['resourcename'])
    assert "resource@x.fr" not in resource1.zimbraPrefCalendarForwardInvitesTo

def test_deleteResource_cas_normal(test_config):
    newResource = ResourceService.deleteResource(test_config['resourcename'])
    resource = ResourceService.getResource(test_config['resourcename'])
    assert resource == None

def test_deleteResource_cas_resource_inexistant(test_config):
    with pytest.raises(ServiceException):
        resource = ResourceService.deleteResource(test_config['resourcename'])
