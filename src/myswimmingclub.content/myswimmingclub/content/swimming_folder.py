
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.supermodel import model
from Products.Five import BrowserView

from myswimmingclub.content import MessageFactory as _

# date formatting
import datetime
from DateTime import DateTime

# View
from plone.memoize.instance import memoize
from myswimmingclub.content.swimming_meet import ISwimmingMeet
from Products.CMFCore.utils import getToolByName

# Static helper methods
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
    elif isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
    if isinstance(end_date, DateTime):
        end_date = end_date.asdatetime().date()
    elif isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
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

def _has_value(brain, value):
    """@param: a brain
       @param: the value we are checking for
       @return: true if the value exists false otherwise
    """
    if not brain.has_key(value):
        return False

    return brain[value] and True or False

def get_folder_contents(view):
    """Get all child contents in this swimming folder.
    """
    types = [ [ 'myswimmingclub.content.swimmingfolder',
                'sortable_title' ],
              [ 'myswimmingclub.content.poollocation',
                'sortable_title' ],
              [ ( 'Event', 'myswimmingclub.content.swimmingmeet'),
                'start' ]
            ]

    catalog = getToolByName(view.context, 'portal_catalog')
    contents = []
    for (portal_type,sort_on) in types:
        query = { 'portal_type': portal_type,
                'path': dict(query='/'.join(view.context.getPhysicalPath()),
                     depth=1),
                'sort_on': sort_on }
        for brain in catalog.searchResults(query):
            d = dict(url=brain.getURL(),
                type= brain.Type,
                title=brain.Title,
                description=brain.Description,)
            #    address_line_1=u'-',
            #    post_or_zip_code=u'-',)
            
            # check for Event or Swimming Meet
            if _has_value(brain,'start') and _has_value(brain,'end'):
                d.update(date_range_formatted=formatDateRange(brain.start, brain.end))
            if _has_value(brain,'address_line_1'):
                d.update(address_line_1=brain.address_line_1)
            if _has_value(brain,'post_or_zip_code'):
                d.update(post_or_zip_code=brain.post_or_zip_code)
            """ check for Swimming Meet 
            """
            if brain.Type is not None and brain.Type == 'Swimming Meet':
                if _has_value(brain,'organisers_entry_date') and _has_value(brain,'club_entry_date'):
                    """ use the earliest entry date
                    """
                    entry_date = brain.club_entry_date
                    if brain.organisers_entry_date < brain.club_entry_date:
                        entry_date = brain.organisers_entry_date
                    d.update(days_left=daysLeft(entry_date))
                    d.update(days_left_formatted=formatDaysLeft(entry_date))
                else:
                    d.update(days_left=-1)
                    d.update(days_left_formatted=_('Entry Date tbc'))
            if brain.Type is not None and brain.Type == 'Pool Location':
                d.update(description=u'Some street, XX11 1YY')
                     
            contents.append(d)
    return contents

# Interface class; used to define content-type schema.
class ISwimmingFolder(model.Schema, IImageScaleTraversable):
    """
    Folderish content type to contain Swimming Meets
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/swimming_folder.xml to define the content type.

    model.load("models/swimming_folder.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class SwimmingFolder(Container):

    # Add your class methods and properties here
    pass


# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@sampleview

class EventPanelView(BrowserView):
    """ sample view class """

    # Add view methods here

    def __call__(self):
        """Called before rendering the template for this view
        """
        self.haveContents       = len(self.folder_contents()) > 0
        return self.index()
    
    @memoize
    def folder_contents(self):
        """Get all child contents in this swimming folder.
        """
        return get_folder_contents(self)

