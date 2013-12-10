from five import grok
from zope import schema
from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from copsclub.content import _

class ILocation(form.Schema):
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

