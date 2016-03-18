
class MigrationFactory:
    def getMigrationContext(self, source=None):
        from plone.dexterity.utils import createObject
        import datetime
        context = None
        target = source.copy()
        portal_type = target.pop('portal_type') \
                         if target.has_key('portal_type') else None
        if portal_type == 'copsclub.swimmingfolder':
            context = createObject('myswimmingclub.content.swimmingfolder', \
                         **target) 
        elif portal_type == 'copsclub.location':
            if target.has_key('title') & target.has_key('post_or_zip_code'):
                target['google_api_query'] = target['title'] + ' ' + \
                                             target['post_or_zip_code']
            elif target.has_key('title'): 
                target['google_api_query'] = target['title']
            elif target.has_key('post_or_zip_code'):
                target['google_api_query'] = target['post_or_zip_code']
            else:
                target['google_api_query'] = ''
            context = createObject('myswimmingclub.content.poollocation', \
                         **target) 
        elif portal_type == 'copsclub.swimmingmeet':
            start = target.pop('start_date')
            end = target.pop('end_date')
            if target.has_key('locations'):
                locations = target.pop('locations')
            target['start'] = datetime.datetime.combine( start,
                                       datetime.time.min)
            target['end'] = datetime.datetime.combine( end,
                                       datetime.time.min)
            context = createObject('myswimmingclub.content.swimmingmeet', \
                         **target) 
        else:
            raise ValueError('Invalid portal_type value')


        return context

#: Private attributes we add to the export list
EXPORT_ATTRIBUTES = ["portal_type", "id"]
class DexterityData:
    _items = None
    def __init__(self, obj):
        self._items = dict()
        for k,v in self.grabDexterityData(obj).items():
            if v != None:
                self._items[k] = v
    
    def items(self):
        return self._items

    def grabDexterityData(self, obj):
        """
        Export Dexterity schema data as dictionary object.
        Snippets taken from
        https://www.andreas-jung.com/contents
        """
        data = {}
        for key in EXPORT_ATTRIBUTES:
            data[key] = getattr(obj, key, None)

        from plone.dexterity.interfaces import IDexterityFTI
        from plone.behavior.interfaces import IBehaviorAssignable
        from zope.component import getUtility
        schema = getUtility(IDexterityFTI, name=obj.portal_type).lookupSchema()
        fields = [(name, schema, schema[name]) for name in schema]

        assignable = IBehaviorAssignable(obj)
        for behavior in assignable.enumerateBehaviors():
            behavior_schema = behavior.interface
            for name in behavior_schema:
                fields.append((name, behavior_schema, behavior_schema[name]))

        for name, schema_adaptor, field in fields:
            source_adapted = schema_adaptor(obj)
            data[name] = getattr(source_adapted, field.getName())
        return data

class Migrator:
    def create_obj(self,source_obj=None, target_parent=None, transition=True):
        from plone import api
        from plone.dexterity.content import Container
        from plone.dexterity.content import Item
        from plone.dexterity.utils import addContentToContainer
        target_obj = None
        # is the source a Dexterity object
        if isinstance(source_obj,Container) or isinstance(source_obj, Item):
            # Dexterity
            source_data = DexterityData(source_obj).items()
            expires = source_data.pop('expires') \
                          if source_data.has_key('expires') else None
            mf = MigrationFactory()
            context = mf.getMigrationContext(source_data)
            target_obj = addContentToContainer(target_parent,context)
            if expires:
                target_obj.setExpirationDate(expires)
        else:
            # Archetype
            # api.copy doesn't return the target_obj so we use container 
            # methods instead

            source_id = source_obj.getId()
            ids = target_parent.manage_pasteObjects(source_obj.manage_copyObjects(source_id))
            if ids[0]['new_id'] == ids[0]['id']:
                target_obj = target_parent[source_id]
            else:
                from zope.container.interfaces import INameChooser
                chooser = INameChooser(target_parent)
                new_id = chooser.chooseName(source_id, source_obj)
                target_parent.manage_renameObject(ids[0]['new_id'], new_id)
                target_obj = target_parent[new_id]

        if (target_obj != None) & transition:
            # state = api.content.get_state(source_obj)
            # if state == u'internal':
            #     api.content.transition(target_obj, transition=u'publish_internaly')
            # elif state == u'external':
            #     api.content.transition(target_obj, transition=u'submit')
            #     api.content.transition(target_obj, transition=u'publish_externally')
            from Products.CMFCore.utils import getToolByName
            workflowTool = getToolByName(api.portal.get(),'portal_workflow')
            print "/".join(source_obj.getPhysicalPath())
            status = workflowTool.getStatusOf('intranet_workflow',source_obj)
            if status: 
                state = status['review_state']
                if state == u'internal':
                    workflowTool.doActionFor(target_obj,'publish_internally')
                elif state == u'external':
                    workflowTool.doActionFor(target_obj,'submit')
                    workflowTool.doActionFor(target_obj,'publish_externally')
        return target_obj

    def walk(self,source_parent, target_parent):
        from Products.CMFCore.interfaces import IFolderish
        for source_obj in source_parent.listFolderContents():
            target_obj = self.create_obj(source_obj, target_parent)
            if IFolderish.providedBy(source_obj):
                self.walk(source_obj, target_obj)

    def migrate(self, source_path):
        from plone import api
        source_obj = api.content.get(path=source_path)
        parent = source_obj.getParentNode()
        target_obj = self.create_obj(source_obj,parent)
        self.walk(source_obj,target_obj)

def migrate_script(path):
    """ Command line helper function.

    Using from the command line::

        bin/instance script migrator.py yoursiteid/path/to/folder

    :param path: Full ZODB path to the folder
    """
    migrator = Migrator()
    migrator.migrate(path)

# Detect if run as a bin/instance run script
if "app" in globals():
    migrate_script(sys.argv[3])
