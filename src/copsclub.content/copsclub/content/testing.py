from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig

class COPSClubContent(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import copsclub.content
        xmlconfig.file('configure.zcml', copsclub.content, context=configurationContext)
    
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'copsclub.content:default')

COPSCLUB_CONTENT_FIXTURE = COPSClubContent()
COPSCLUB_CONTENT_INTEGRATION_TESTING = IntegrationTesting(bases=(COPSCLUB_CONTENT_FIXTURE,), name="COPSClubContent:Integration")
