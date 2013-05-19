import unittest2 as unittest
from copsclub.policy.testing import COPSCLUB_POLICY_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName

class TestSetup(unittest.TestCase):
    
    layer = COPSCLUB_POLICY_INTEGRATION_TESTING
    
    def test_portal_title(self):
        portal = self.layer['portal']
        self.assertEqual("City of Peterborough Swimming Club", portal.getProperty('title'))
    
    def test_portal_description(self):
        portal = self.layer['portal']
        self.assertEqual("Welcome to City of Peterborough Swimming Club", portal.getProperty('description'))

    def test_role_added(self):
        portal = self.layer['portal']
        self.assertTrue("Coach" in portal.validRoles())
    
    def test_workflow_installed(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertTrue('copsclub_publication_workflow' in workflow)
    
# ------------------------------------------------------------------------
# Remove assignment of the publication workflow on the News Item
# ------------------------------------------------------------------------
#    def test_workflows_news(self):
#        portal = self.layer['portal']
#        workflow = getToolByName(portal, 'portal_workflow')
#        self.assertEqual(('copsclub_publication_workflow',), workflow.getChainFor('News Item'))
    
    def test_view_permisison_for_coach(self):
        portal = self.layer['portal']
        self.assertTrue('View' in [r['name']
            for r in portal.permissionsOfRole('Reader')
            if r['selected']])
        self.assertTrue('View' in [r['name']
            for r in portal.permissionsOfRole('Coach')
            if r['selected']])

# ------------------------------------------------------------------------
# Remove the role map for coach onto News Item
# ------------------------------------------------------------------------
#    
#    def test_add_news_permisison_for_coach(self):
#        portal = self.layer['portal']
#        self.assertTrue('ATContentTypes: Add News Item' in [r['name']
#            for r in portal.permissionsOfRole('Reader')
#            if r['selected']])
#        self.assertTrue('ATContentTypes: Add News Item' in [r['name']
#            for r in portal.permissionsOfRole('Coach')
#            if r['selected']])

    def test_access_contents_information_permisison_for_coach(self):
        portal = self.layer['portal']
        self.assertTrue('Access contents information' in [r['name']
            for r in portal.permissionsOfRole('Reader')
            if r['selected']])
        self.assertTrue('Access contents information' in [r['name']
            for r in portal.permissionsOfRole('Coach')
            if r['selected']])

    def test_coaches_group_added(self):
        portal = self.layer['portal']
        acl_users = portal['acl_users']
        self.assertEqual(1, len(acl_users.searchGroups(name='Coaches')))

    def test_authors_group_added(self):
        portal = self.layer['portal']
        acl_users = portal['acl_users']
        self.assertEqual(1, len(acl_users.searchGroups(name='Authors')))
