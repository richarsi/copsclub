import datetime
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

class ISwimmingFolder(form.Schema):
    """A folder that can contain swimmingmeets
    """
    
    text = RichText(
            title=_(u"Body text"),
            description=_(u"Introductory text for this swimming folder"),
            required=False
        )

class View(grok.View):
    """Default view (called "@@view"") for a swimming folder.
    
    The associated template is found in swimmingfolder_templates/view.pt.
    """
    
    grok.context(ISwimmingFolder)
    grok.require('zope2.View')
    grok.name('view')
    
    def update(self):
        """Called before rendering the template for this view
        """
        
        self.haveSwimmingMeets       = len(self.swimmingmeets()) > 0
    
    @memoize
    def swimmingmeets(self):
        """Get all child swimmingmeets in this swimming folder.
        """
        results = []
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'object_provides': ISwimmingMeet.__identifier__,
                    'path': dict(query='/'.join(self.context.getPhysicalPath()),
                         depth=1),
                    'sort_on': 'start'}
        for swimmingmeet in catalog.searchResults(query):
            start_date=swimmingmeet.start_date
            end_date=swimmingmeet.end_date
            # Create the formatted output for the event date
            # if same date then
            #     output = dd mmm
            # else if same month
            #     output = dd_start - dd_end mmm (e.g. 27 - 28 March)
            # else
            #     output = dd_start mmm_start - dd_end mmm_end
            date_range_formatted = "Date Error"
            if start_date == end_date:
                date_range_formatted = start_date.strftime("%d %b %Y")
            else:
                if start_date.month == end_date.month:
                    date_range_formatted = start_date.strftime("%d") + " - " + end_date.strftime("%d %b %Y")
                else:
                    date_range_formatted = start_date.strftime("%d %b") + " - " + end_date.strftime("%d %b %Y")

            # Create the formatted output for days left to enter the meet
            # if days remaining is == 1
            #     output = "1 day left"
            # else if days remaining is > 1
            #     output = "dd days left"
            # else
            #     output = "Entry Closed"
            days_left_formatted = "Entry Closed"
            today = datetime.datetime.now().date()
            days_left = (swimmingmeet.organisers_entry_date - today).days
            if (days_left == 1):
                days_left_formatted = "%d day left to enter" % days_left
            else:
                if (days_left > 1):
                    days_left_formatted = "%d days left to enter" % days_left

            # Build the locations
#            locations = []
#            if swimmingmeet.locations is not None:
#                for ref in swimmingmeet.locations:
#                    obj = ref.to_object
#                    locations.append({
#                            'url': obj.absolute_url(),
#                            'title': obj.title,
#                        })
#
#            print locations

            results.append( dict(url=swimmingmeet.getURL(),
                      type=swimmingmeet.Type,
                      title=swimmingmeet.Title,
                      description=swimmingmeet.Description,
                      start_date=swimmingmeet.start_date,
                      end_date=swimmingmeet.end_date,
                      organisers_entry_date=swimmingmeet.organisers_entry_date,
                      club_entry_date=swimmingmeet.club_entry_date,
#                      locations=locations,
                      date_range_formatted=date_range_formatted,
                      days_left_formatted=days_left_formatted,
                      days_left=days_left,)
                )
        return results

# You can use this method to add a portlet which would be able to display
# a list of the meets that were nearing thier cut off date. Or you could 
# use it to promote an event... 
# 
# @grok.subscribe(ISwimmingFolder, IObjectAddedEvent)
# def addPromotionsPortlet(obj, event):
#     """Event handler triggered when adding a swimming folder. This will add
#        the promotions portlet automatically.
#     """
#     
#     # Only do this if the parent is not a swimming folder, i.e. only do it on
#     # top-level swimming folders. Of course, site managers can move things 
#     # around once the site structure is created
#     
#     parent = aq_parent(obj)
#     if ISwimmingFolder.providedBy(parent):
#         return
#     
#     # A portlet manager is akin to a column
#     column = getUtility(IPortletManager, name=PROMOTIONS_PORTLET_COLUMN)
#     
#     # We multi-adapt the object and the column to an assignment mapping,
#     # which acts like a dict where we can put portlet assignments
#     manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
#     
#     # We then create the assignment and put it in the assignment manager,
#     # using the default name-chooser to pick a suitable name for us.
#     assignment = promotions.Assignment()
#     chooser = INameChooser(manager)
#     manager[chooser.chooseName(None, assignment)] = assignment
