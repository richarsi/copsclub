from five import grok
from zope import schema
from plone.supermodel import model
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from copsclub.content import _

class ISquad(model.Schema, IImageScaleTraversable):
    """A content item to hold squad details as used by the SwimmingMeet content type
    """
    
    code = schema.TextLine (
            title=_(u"Code"),
            min_length=2,
            max_length=2,
            description=_(u"A 2 digit code which is used to uniquely identify the squad"),
            required=True
        )
    information = RichText (
            title=_(u"Information"),
            description=_(u"Some information about the squad"),
            required=False
        )
    image = NamedBlobImage(
            title=_(u"Squad image icon"),
            description=_(u"An image used for this swimming squad when displayed with the swimming meet"),
        )
