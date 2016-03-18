from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base

from datetime import datetime

class ISwimmingMeetPortlet(IPortletDataProvider):

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    state = schema.Tuple(title=_(u"Workflow state"),
                         description=_(u"Items in which workflow state to show."),
                         default=('published', ),
                         required=True,
                         value_type=schema.Choice(
                             vocabulary="plone.app.vocabularies.WorkflowStates")
                         )


class Assignment(base.Assignment):
    implements(ISwimmingMeetPortlet)

    def __init__(self, count=5, state=('published', )):
        self.count = count
        self.state = state

    @property
    def title(self):
        return _(u"SwimmingMeet")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('swimmingmeet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return self.data.count > 0 and len(self._data())

    def published_swimming_meet_items(self):
        return self._data()

    def all_swimming_meet_link(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
            name='plone_portal_state')
        portal = portal_state.portal()
        # Find the first 'Swimming Folder' on the root of the site 
        navigation_root_path = portal_state.navigation_root_path()
        catalog = getToolByName(context, 'portal_catalog')
        query = { 'portal_type': 'myswimmingclub.content.swimmingfolder',
                'path': dict(query=navigation_root_path, depth=1),
                'sort_on': 'created' }
        swimming_folders = catalog.searchResults(query)
        # import pdb; pdb.set_trace()
        if swimming_folders:
            swimming_folder = swimming_folders[0]['id']
            return '%s/%s' % (portal_state.navigation_root_url(), swimming_folder)
        return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((context, self.request),
            name='plone_portal_state')
        path = portal_state.navigation_root_path()
        limit = self.data.count
        state = self.data.state
        date_range = { 'query': datetime.today(), 'range': 'min' } 
        query = { 'portal_type': ('Event',
                                  'myswimmingclub.content.swimmingmeet'),
                  'review_state': state,
                  'path': path,
                  'start': date_range,
                  'sort_on': 'start',
                  'sort_limit': limit }
        return catalog.searchResults(query)[:limit]


class AddForm(base.AddForm):
    form_fields = form.Fields(ISwimmingMeetPortlet)
    label = _(u"Add Swimming Meet Portlet")
    description = _(u"This portlet displays recent Swimming Meet items.")

    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published', )))


class EditForm(base.EditForm):
    form_fields = form.Fields(ISwimmingMeetPortlet)
    label = _(u"Edit SwimmingMeet Portlet")
    description = _(u"This portlet displays recent Swimming Meet items.")
