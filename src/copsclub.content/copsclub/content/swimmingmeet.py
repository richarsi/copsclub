from datetime import datetime
from five import grok
from plone.app.textfield import RichText
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from z3c.relationfield.schema import RelationList, RelationChoice
from zope import schema

from copsclub.content.location import ILocation
from copsclub.content.squad import ISquad

from copsclub.content import _

# Validators
from z3c.form import validator
import zope.component

# View
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName

# Indexer
from plone.indexer import indexer

class ISwimmingMeet(model.Schema, IImageScaleTraversable):
    """A folder that can contain files
    """

    # form.widget(locations=AutcompleteFieldWidget)
    locations = RelationList (
            title=_(u"Locations"),
            description=_(u"Locations of the swimming meet"),
            value_type=RelationChoice(
                    source=ObjPathSourceBinder(
                            object_provides=ILocation.__identifier__
                        ),
                ),
            required=False,
        )
    
    start_date = schema.Date (
            title=_(u"Swimming start date"),
            description=_(u"The first day of the swimming meet"),
            required=True
        )
    end_date = schema.Date (
            title=_(u"Swimming end date"),
            description=_(u"The last day for the swimming meet"),
            required=True
        )
    age_as_of_date = schema.Date (
            title=_(u"Swimming age as of  date"),
            description=_(u"The date for determining the age of the swimmer"),
            required=True
        )
    organisers_entry_date = schema.Date (
            title=_(u"Organisers entry date"),
            description=_(u"The date the organisers close entry to the meet"),
            required=True
        )
    club_entry_date = schema.Date (
            title=_(u"Club entry date"),
            description=_(u"The date this club stops accepting entries"),
            required=True
        )
    
    #form.widget(squads=AutocompleteFieldWidget)
    squads = RelationList(
            title=_(u"Squads"),
            description=_(u"A list of squads that the meet is applicable for"),
            value_type=RelationChoice(
                    source=ObjPathSourceBinder(
                            object_provides=ISquad.__identifier__
                        ),
                ),
            required=False,
        )

    team_manager = schema.TextLine (
            title=_(u"Team Manager"),
            description=_(u"The team manager for the swimming meet"),
            required=True
        )

#
# VALIDATORS
#

# dates must be after 1st Jan 2010
class DateValidator(validator.SimpleFieldValidator):
    """ z3c.form validator class for dates """

    def validate(self,value):
        """ validate dates > 1 Jan 2010 """
        if value != None:
            if value < datetime(2010,01,01).date():
                raise zope.interface.Invalid(_(u"Date must be greater than 1st Jan 2010"))


# Set conditions for which fields the validator class applies
# validator.WidgetValidatorDiscriminators(DateValidator, field=ISwimmingMeet['start_date'])
validator.WidgetValidatorDiscriminators(DateValidator, field=schema.Date)

# Register the validator so it will be looked up by z3c.form machinery
zope.component.provideAdapter(DateValidator)

@indexer(ISwimmingMeet)
def swimmingmeetStartIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``start`` index with the swimmingmeet's start date.
    """
    return context.start_date
grok.global_adapter(swimmingmeetStartIndexer, name='start')

@indexer(ISwimmingMeet)
def swimmingmeetEndIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``end`` index with the swimmingmeet's end date.
    """
    return context.end_date
grok.global_adapter(swimmingmeetEndIndexer, name='end')

class View(grok.View):
    """Default view (called "@@view"") for a swimmingmeet.
    
    The associated template is found in swimmingmeet_templates/view.pt.
    """
    
    grok.context(ISwimmingMeet)
    grok.require('zope2.View')
    grok.name('view')
    
    def update(self):
        """Prepare information for the template
        """
        self.haveLocations = len(self.locations()) > 0
        self.haveSquads    = len(self.squads()) > 0
        self.start_date_formatted = self.context.start_date.strftime("%d %b %Y")
        self.end_date_formatted = self.context.end_date.strftime("%d %b %Y")
        self.age_as_of_date_formatted = self.context.age_as_of_date.strftime("%d %b %Y")
        self.organisers_entry_date_formatted = self.context.organisers_entry_date.strftime("%d %b %Y")
        self.club_entry_date_formatted = self.context.club_entry_date.strftime("%d %b %Y")
        self.haveFiles    = len(self.files()) > 0
    
    @memoize
    def locations(self):
        
        locs = []
        
        if self.context.locations is not None:
            for ref in self.context.locations:
                obj = ref.to_object
                # be defensive
                if obj is None:
                     continue
            
                locs.append({
                        'url': obj.absolute_url(),
                        'title': obj.title,
                        'summary': obj.description,
                    })
        
        return locs
        
    @memoize
    def squads(self):
        
        s = []
        
        if self.context.squads is not None:
            for ref in self.context.squads:
                obj = ref.to_object
                # be defensive
                if obj is None:
                     continue
            
                scales = getMultiAdapter((obj, self.request), name='images')
                scale = scales.scale('image', scale='tile')
                imageTag = None
                if scale is not None:
                    imageTag = scale.tag()
            
                s.append({
                        'url': obj.absolute_url(),
                        'title': obj.title,
                        'summary': obj.description,
                        'imageTag': imageTag,
                    })
        
        return s

    @memoize
    def files(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())
        results = catalog(path={'query': folder_path, 'depth': 1})
        f = []
        if results is not None:
            for brain in results:

                f.append({
                        'url': brain.getURL(),
                        'title': brain["Title"],
                        'summary': brain["Description"],
                        'meta_type': brain["meta_type"],
                        'size': brain["getObjSize"],
                        'icon': brain["getIcon"],
                    })
        
        return f
