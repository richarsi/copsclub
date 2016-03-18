from myswimmingclub.content import MessageFactory as _
from zope.interface import Interface
from zope import schema

class IMySwimmingClubSettings(Interface):
    """Describes registry records
    """
    apiCode = schema.Text(
        title=_(u"Google Maps API code"),
        description=_(u"The Google Maps API code, which you can find by visiting your Google Maps API dashboard."),
    )
    swimmingEvents = schema.Tuple (
        title=_(u"Swimming events"),
        description=_(u"Allowable event that can be swum at a Swimming Meet. To be entered one per line as code|description e.g. 50Free|50m Freestyle."),
        value_type=schema.TextLine(),
    )
