from five import grok
from zope import schema
from plone.directives import form, dexterity

from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget

from copsclub.content.location import ILocation

from copsclub.content import _

class ISwimmingMeet(form.Schema):
    """A folder that can contain cinemas
    """

    form.widget(location=AutocompleteFieldWidget)
    location = RelationChoice (
            title=_(u"Location"),
            description=_(u"Location of the swimming meet"),
            source=ObjPathSourceBinder(
                    object_provides=ILocation.__identifier__
                ),
            required=False,
        )
    
    start = schema.Date (
            title=_(u"Swimming start date."),
            description=_(u"The description for the swimming meet"),
            required=True
        )
    end = schema.Date (
            title=_(u"Swimming end date."),
            description=_(u"The end date for the swimming meet"),
            required=True
        )
    age_as_of = schema.Date (
            title=_(u"Swimming age as of  date"),
            description=_(u"The age as of date for the swimming meet"),
            required=True
        )
    organisers_entry_expiry_date = schema.Date (
            title=_(u"Organisers entry expiry date."),
            description=_(u"The organisers entry expiry date"),
            required=True
        )
    club_entry_expiry_date = schema.Date (
            title=_(u"COPS entry expiry date"),
            description=_(u"COPS entry expiry date"),
            required=True
        )
    team_manager = schema.TextLine (
            title=_(u"Team Manager"),
            description=_(u"The team manager for the swimming meet."),
            required=True
        )

