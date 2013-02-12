from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig

class CopsClubPolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import copsclub.policy
        xmlconfig.file('configure.zcml', copsclub.policy, context=configurationContext)
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'copsclub.policy:default')

COPSCLUB_POLICY_FIXTURE = CopsClubPolicy()
COPSCLUB_POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(COPSCLUB_POLICY_FIXTURE,), name="CopsClub:Integration")
