import transaction
import logging
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from z3c.relationfield.event import updateRelations
from z3c.relationfield.interfaces import IHasRelations
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

''' Upgrade to version 1001
    reindex zc.relations catalog
'''
rcatalog = getUtility(ICatalog)
# Clear the relation catalog to fix issues with interfaces that don't exist anymore.
# This actually fixes the bug editing employees than reports a:
#   KeyError: <class 'plone.directives.form.schema.Schema'>

transaction.begin()
rcatalog.clear()

site = app.get('Plone')
catalog = getToolByName(site, 'portal_catalog')
brains = catalog.searchResults(object_provides=IHasRelations.__identifier__)

for brain in brains:
    logger.info(obj)
    obj = brain.getObject()
    updateRelations(obj, None)
transaction.commit()
