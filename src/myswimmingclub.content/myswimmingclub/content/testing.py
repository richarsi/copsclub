from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig

class MySwimmingClubContent(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import myswimmingclub.content
        xmlconfig.file('configure.zcml', myswimmingclub.content,
        context=configurationContext)
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'myswimmingclub.content:default')

MYSWIMMINGCLUB_CONTENT_FIXTURE = MySwimmingClubContent()
MYSWIMMINGCLUB_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
        bases=(MYSWIMMINGCLUB_CONTENT_FIXTURE,),
        name="MySwimmingClubContent:Integration"
    )
