from five import grok
from zope import schema
from plone.supermodel import model
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from plone.namedfile.interfaces import IImageScaleTraversable

# View
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize

from copsclub.content import _

class ILocation(model.Schema, IImageScaleTraversable):
    """A content item to hold location details as used by the SwimmingMeet content type
    """
    
    address_line_1 = schema.TextLine (
            title=_(u"Address Line 1"),
            description=_(u"The first line of the address"),
            required=True
        )
    address_line_2 = schema.TextLine (
            title=_(u"Address Line 2"),
            description=_(u"The second line of the address"),
            required=False
        )
    address_line_3 = schema.TextLine (
            title=_(u"Address Line 3"),
            description=_(u"The third line of the address"),
            required=False
        )
    town_or_city = schema.TextLine (
            title=_(u"Town or City"),
            description=_(u"Town or city"),
            required=False
        )
    county_or_state = schema.TextLine (
            title=_(u"County or State"),
            description=_(u"County or state"),
            required=False
        )
    post_or_zip_code = schema.TextLine (
            title=_(u"Post or ZIP Code"),
            description=_(u"Post or ZIP code"),
            required=False
        )

    details = RichText (
            title=_(u"Details"),
            description=_(u"Some details about the location"),
            required=False
        )

class View(grok.View):
    """Default view (called "@@view"") for a lcoation.
    
    The associated template is found in lcoation_templaten/view.pt.
    """
    
    grok.context(ILocation)
    grok.require('zope2.View')
    grok.name('view')

    @memoize
    def location_lines(self):
        l = []
        if self.context.address_line_1 is not None:
            l.append(self.context.address_line_1)
        if self.context.address_line_2 is not None:
            l.append(self.context.address_line_2)
        if self.context.address_line_3 is not None:
            l.append(self.context.address_line_3)
        if self.context.town_or_city is not None:
            l.append(self.context.town_or_city)
        if self.context.county_or_state is not None:
            l.append(self.context.county_or_state)
        if self.context.post_or_zip_code is not None:
            l.append(self.context.post_or_zip_code)
        
        return l
