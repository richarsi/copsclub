from five import grok
from zope import schema
from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from copsclub.content import _

class ISquad(form.Schema):
    """A content item to hold squad details as used by the SwimmingMeet content type
    """
    
    code = schema.TextLine (
            title=_(u"Code"),
            min_length=2,
            max_length=2,
            description=_(u"A 2 digit code which is used to uniquely identify the squad"),
            required=True
        )
    information = schema.Text (
            title=_(u"Information"),
            description=_(u"Some information about the squad"),
            required=False
        )
