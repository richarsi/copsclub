import datetime
from DateTime import DateTime
from five import grok
from zope import schema
from plone.directives import form

from plone.app.textfield import RichText

from copsclub.content import _

# View
from plone.memoize.instance import memoize
from copsclub.content.swimmingmeet import ISwimmingMeet
from Products.CMFCore.utils import getToolByName

# Subscriber
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.container.interfaces import INameChooser

from zope.lifecycleevent.interfaces import IObjectAddedEvent

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from Acquisition import aq_parent

def formatDateRange(start_date, end_date):
    # Create the formatted output for the event date
    # if same date then
    #     output = dd mmm
    # else if same month
    #     output = dd_start - dd_end mmm (e.g. 27 - 28 March)
    # else
    #     output = dd_start mmm_start - dd_end mmm_end
    if isinstance(start_date, DateTime):
        start_date = start_date.asdatetime().date()
    if isinstance(end_date, DateTime):
        end_date = end_date.asdatetime().date()
    date_range_formatted = "Date Error"
    if (start_date is not None) and (end_date is not None):
        if start_date == end_date:
            date_range_formatted = start_date.strftime("%d %b %Y")
        else:
            if start_date.month == end_date.month:
                date_range_formatted = start_date.strftime("%d") + " - " + end_date.strftime("%d %b %Y")
            else:
                date_range_formatted = start_date.strftime("%d %b") + " - " + end_date.strftime("%d %b %Y")
    return date_range_formatted
        
def daysLeft(test_date):
    days_left = None
    today = datetime.datetime.now().date()
    # if ((test_date is not None) and (isinstance(test_date, datetime.date))):
    if (test_date is not None):
        days_left = (test_date - today).days
    else:
        days_left = -9999
    return days_left
        
def formatDaysLeft(test_date):
    # Create the formatted output for days left to enter the meet
    # if days remaining is == 1
    #     output = "1 day left"
    # else if days remaining is > 1
    #     output = "dd days left"
    # else
    #     output = "Entry Closed"
    days_left = daysLeft(test_date)
    days_left_formatted = "Entry Closed"
    if (days_left == 1):
        days_left_formatted = "1 day left to enter"
    else:
        if (days_left > 1):
           days_left_formatted = "%d days left to enter" % days_left
    return days_left_formatted

def get_folder_contents(view):
    """Get all child contents in this swimming folder.
    """
    catalog = getToolByName(view.context, 'portal_catalog')

    folders = []
    query = { 'portal_type': 'copsclub.swimmingfolder',
                'path': dict(query='/'.join(view.context.getPhysicalPath()),
                     depth=1),
                'sort_on': 'sortable_title' }
    for folder in catalog.searchResults(query):
        folders.append( dict(url=folder.getURL(),
                  type= folder.Type,
                  title=folder.Title,
                  description=folder.Description,)
            )

    locations = []
    query = { 'portal_type': 'copsclub.location',
                'path': dict(query='/'.join(view.context.getPhysicalPath()),
                     depth=1),
                'sort_on': 'sortable_title' }
    for location in catalog.searchResults(query):
        locations.append( dict(url=location.getURL(),
                  type= location.Type,
                  title=location.Title,
                  description=location.Description,)
            )

    """Get all child Events and copsclub.swimmingmeets in this swimming folder.
    """
    results = []
    query = { 'portal_type': ( 'Event', 'copsclub.swimmingmeet' ),
                'path': dict(query='/'.join(view.context.getPhysicalPath()),
                     depth=1),
                'sort_on': 'start'}
    for event in catalog.searchResults(query):
        if event.Type is not None and event.Type == 'Swimming Meet':
            entry_date = event.club_entry_date
            if event.organisers_entry_date < event.club_entry_date:
                entry_date = event.organisers_entry_date
            results.append( dict(url=event.getURL(),
                      type= event.Type,
                      title=event.Title,
                      description=event.Description,
                      date_range_formatted=formatDateRange(event.start, event.end),
                      days_left=daysLeft(entry_date),
                      days_left_formatted=formatDaysLeft(entry_date))
                )
        else:
           results.append( dict(url=event.getURL(),
                     type= event.Type,
                     title=event.Title,
                     description=event.Description,
                     date_range_formatted=formatDateRange(event.start, event.end))
               )
    return folders + locations + results
    
class ISwimmingFolder(form.Schema):
    """A folder that can contain swimmingmeets
    """

class EventPanelView(grok.View):
    """A new view for a swimming folder.
    
    The associated template is found in swimmingfolder_templates/event_panel_view.pt.
    """
    
    grok.context(ISwimmingFolder)
    grok.require('zope2.View')
    grok.name('event_panel_view')

    def update(self):
        """Called before rendering the template for this view
        """
        
        self.haveContents       = len(self.folder_contents()) > 0
    
    @memoize
    def folder_contents(self):
        """Get all child contents in this swimming folder.
        """
        return get_folder_contents(self)

