
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
from plone.dexterity.browser.view import DefaultView

# add support for iCal and vCal to the view
from cStringIO import StringIO
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin

from Acquisition import aq_inner
import datetime
import DateTime

# for viewlets
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from myswimmingclub.content import MessageFactory as _

# Interface class; used to define content-type schema.

class ISwimmingMeet(model.Schema, IImageScaleTraversable):
    """
    Swimming Meet content type for My Swimming Club
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/swimming_meet.xml to define the content type.

    model.load("models/swimming_meet.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class SwimmingMeet(Container):

    # Add your class methods and properties here

    # Static helper methods
    def getDateTime(self, dt):
        if dt or isinstance(dt, datetime.date):
            return  DateTime.DateTime(datetime.datetime.combine( dt, datetime.time.min))
        else:
            return None

    def formatDateRange(self):
        # Create the formatted output for the event date
        # if same date then
        #     output = dd mmm
        # else if same month
        #     output = dd_start - dd_end mmm (e.g. 27 - 28 March)
        # else
        #     output = dd_start mmm_start - dd_end mmm_end
        start_date = self.start
        end_date = self.end
        if isinstance(start_date, DateTime.DateTime):
            start_date = start_date.asdatetime().date()
        elif isinstance(start_date, datetime.datetime):
            start_date = start_date.date()
        if isinstance(end_date, DateTime.DateTime):
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
            
    def daysLeft(self):
        days_left = None
        test_date = self.club_entry_date
        today = datetime.datetime.now().date()
        # if ((test_date is not None) and (isinstance(test_date, datetime.date))):
        if (test_date is not None):
            days_left = (test_date - today).days
        else:
            days_left = -9999
        return days_left
            
    def formatDaysLeft(self):
        # Create the formatted output for days left to enter the meet
        # if days remaining is == 1
        #     output = "1 day left"
        # else if days remaining is > 1
        #     output = "dd days left"
        # else
        #     output = "Entry Closed"
        days_left = self.daysLeft()
        days_left_formatted = "Entry Closed"
        if (days_left == 1):
            days_left_formatted = "1 day left to enter"
        else:
            if (days_left > 1):
               days_left_formatted = "%d days left to enter" % days_left
        return days_left_formatted
    

# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@sampleview


class SampleView(BrowserView):
    """ sample view class """

    # Add view methods here

class SwimmingMeetView(BrowserView):
    """ sample view class """

    def update(self):
        self.haveLocations = len(self.locations()) > 0

    def locations(self):
        locations = []
        if self.context.location is not None:
            for ref in self.context.location:
                obj = ref.to_object
                locations.append( {
                    'url': obj.absolute_url(),
                    'title': obj.title,
                    'summary': obj.description,
                    'GoogleMap': obj.getGoogleMap(),
                    'address': [ obj.address_line_1, 
                                 obj.address_line_2,
                                 obj.address_line_3,
                                 obj.town_or_city,
                                 obj.county_or_state,
                                 obj.post_or_zip_code,
                               ],
                    'location_url': obj.location_url,
                })
        return locations

class SwimmingMeetMessage(BrowserView):
    """A message displayed in the viewlet above content
    """
    implements(IViewlet)
    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__ = view # from IContentProvider
        self.manager = manager # from IViewlet

    def update(self):
        pass

    render = ViewPageTemplateFile("swimming_meet_templates/message.pt")
        
PRODID = "-//MySwimmingClub Content Types//Swimming Meet//EN"

# iCal header and footer
ICS_HEADER = """\
BEGIN:VCALENDAR
PRODID:%(prodid)s
VERSION:2.0
METHOD:PUBLISH
"""

ICS_FOOTER = """\
END:VCALENDAR
"""

# Note: a previous version of event start set "SEQUENCE:0"
# That's not necessary unless we're supporting recurrence.

# iCal event
ICS_EVENT_START = """\
BEGIN:VEVENT
DTSTAMP:%(dtstamp)s
CREATED:%(created)s
UID:ATEvent-%(uid)s
LAST-MODIFIED:%(modified)s
SUMMARY:%(summary)s
DTSTART:%(startdate)s
DTEND:%(enddate)s
"""

ICS_EVENT_END = """\
CLASS:PUBLIC
END:VEVENT
"""

class ics_view(DefaultView):
    """ return a iCal object """

    def getICal(self):
        """get iCal data
        """
        context = aq_inner(self.context)
        out = StringIO()
        map = {
            'dtstamp': rfc2445dt(DateTime.DateTime()),
            'created': rfc2445dt(DateTime.DateTime(context.CreationDate())),
            'uid': getattr(context, 'UID', None),
            'modified': rfc2445dt(DateTime.DateTime(context.ModificationDate())),
            'summary': vformat(context.Title()),
            'startdate': rfc2445dt(getattr(context, 'start', None)),
            'enddate': rfc2445dt(getattr(context, 'end', None)),
            }
        out.write(ICS_EVENT_START % map)

        description = context.Description()
        if description:
            out.write(foldLine('DESCRIPTION:%s\n' % vformat(description)))

        # location = self.getLocation()
        # if location:
        #     out.write('LOCATION:%s\n' % vformat(location))

        # subject = self.Subject()
        # if subject:
        #     out.write('CATEGORIES:%s\n' % ', '.join(subject))

        # cn = []
        # contact = self.contact_name()
        # if contact:
        #     cn.append(contact)
        # phone = self.contact_phone()
        # if phone:
        #     cn.append(phone)
        # email = self.contact_email()
        # if email:
        #     cn.append(email)
        # if cn:
        #     out.write('CONTACT:%s\n' % vformat(', '.join(cn)))

        # url = self.event_url()
        # if url:
        #     out.write('URL:%s\n' % url)

        out.write(ICS_EVENT_END)
        return out.getvalue()


    def render(self):
        """iCalendar output
        """
        context = aq_inner(self.context)
        self.request.response.setHeader('Content-Type', 'text/calendar')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.ics"' % context.getId())
        out = StringIO()
        out.write(ICS_HEADER % {'prodid': PRODID})
        out.write(self.getICal())
        out.write(ICS_FOOTER)
        return n2rn(out.getvalue())

    def __call__(self):
        return self.render()

# vCal header and footer
VCS_HEADER = """\
BEGIN:VCALENDAR
PRODID:%(prodid)s
VERSION:1.0
"""

VCS_FOOTER = """\
END:VCALENDAR
"""

# vCal event
VCS_EVENT_START = """\
BEGIN:VEVENT
DTSTART:%(startdate)s
DTEND:%(enddate)s
DCREATED:%(created)s
UID:ATEvent-%(uid)s
SEQUENCE:0
LAST-MODIFIED:%(modified)s
SUMMARY:%(summary)s
"""

VCS_EVENT_END = """\
PRIORITY:3
TRANSP:0
END:VEVENT
"""
class vcs_view(DefaultView):
    """ return a vCal object """

    def getVCal(self):
        """get vCal data
        """
        context = aq_inner(self.context)
        out = StringIO()
        map = {
            'dtstamp': rfc2445dt(DateTime.DateTime()),
            'created': rfc2445dt(DateTime.DateTime(context.CreationDate())),
            'uid': getattr(context, 'UID', None),
            'modified': rfc2445dt(DateTime.DateTime(context.ModificationDate())),
            'summary': vformat(context.Title()),
            'startdate': rfc2445dt(getattr(context, 'start', None)),
            'enddate': rfc2445dt(getattr(context, 'end', None)),
            }
        out.write(VCS_EVENT_START % map)
        description = context.Description()
        if description:
            out.write(foldLine('DESCRIPTION:%s\n' % vformat(description)))
        # TODO
        # location = self.getLocation()
        # if location:
        #    out.write('LOCATION:%s\n' % vformat(location))
        out.write(VCS_EVENT_END)
        return out.getvalue()

    def render(self):
        import pdb; pdb.set_trace()
        context = aq_inner(self.context)
        self.request.response.setHeader('Content-Type', 'text/x-vCalendar')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.vcs"' % context.getId())
        out = StringIO()
        out.write(self.getVCal())
        return n2rn(out.getvalue())
        # return self.index() - this is the index page!

    def __call__(self):
        return self.render()

def vformat(s):
    # return string with escaped commas and semicolons
    # NOTE: RFC 2445 specifies "a COLON character in a 'TEXT' property value
    # SHALL NOT be escaped with a BACKSLASH character." So watch out for
    # non-TEXT values, should they be introduced later in this code!
    return s.strip().replace(', ', '\, ').replace(';', '\;')

def n2rn(s):
    return s.replace('\n', '\r\n')

def rfc2445dt(dt):
    # return UTC in RFC2445 format YYYYMMDDTHHMMSSZ
    if isinstance(dt, DateTime.DateTime):
        return dt.HTML4().replace('-', '').replace(':', '')
    elif isinstance(dt, datetime.datetime):
        return DateTime.DateTime(dt).HTML4().replace('-', '').replace(':', '')
    elif isinstance(dt, datetime.date):
        return DateTime.DateTime(datetime.datetime.combine( dt, datetime.time.min)).HTML4().replace('-', '').replace(':', '')
    else:
        return None

def foldLine(s):
    # returns string folded per RFC2445 (each line must be less than 75 octets)
    # This code is a minor modification of MakeICS.py, available at:
    # http://www.zope.org/Members/Feneric/MakeICS/

    lineLen = 70

    workStr = s.strip().replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n')
    numLinesToBeProcessed = len(workStr) / lineLen
    startingChar = 0
    res = ''
    while numLinesToBeProcessed >= 1:
        res = '%s%s\n ' % (res, workStr[startingChar:startingChar + lineLen])
        startingChar += lineLen
        numLinesToBeProcessed -= 1
    return '%s%s\n' % (res, workStr[startingChar:])
 
