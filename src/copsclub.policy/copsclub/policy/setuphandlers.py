from Products.CMFCore.utils import getToolByName
def setupGroups(portal):
    acl_users = getToolByName(portal, 'acl_users')
    if not acl_users.searchGroups(name='Coaches'):
        gtool = getToolByName(portal, 'portal_groups')
        gtool.addGroup('Coaches', roles=['Coach'])
    if not acl_users.searchGroups(name='Authors'):
        gtool = getToolByName(portal, 'portal_groups')
        gtool.addGroup('Authors', roles=['Contributor','Editor'])
def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('copsclub.policy-various.txt') is None:
        return
    portal = context.getSite()
    setupGroups(portal)
