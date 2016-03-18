"""

    Export folder contents as JSON.

    Can be run as a browser view or command line script.

"""

import os
import base64

try:
    import json
except ImportError:
    # Python 2.54 / Plone 3.3 use simplejson
    # version 2.3.3
    import simplejson as json

from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import IFolderish
from DateTime import DateTime
from datetime import datetime
from datetime import date
from plone.app.textfield.value import RichTextValue
from plone.app.blob.field import BlobWrapper
from z3c.relationfield.relation import RelationValue

#: Private attributes we add to the export list
EXPORT_ATTRIBUTES = ["portal_type", "id"]

#: Do we dump out binary data... default we do, but can be controlled with env var
EXPORT_BINARY = os.getenv("EXPORT_BINARY", None)
if EXPORT_BINARY:
    EXPORT_BINARY = EXPORT_BINARY == "true"
else:
    EXPORT_BINARY = True


class ExportFolderAsJSON(BrowserView):
    """
    Exports the current context folder Archetypes as JSON.

    Returns downloadable JSON from the data.
    """

    def convert(self, value):
        """
        Convert value to more JSON friendly format.
        """
        if type(value) is list or type(value) is tuple:
            converted = []
            for item in value:
                 converted.append(self.convert(item))
            return converted
        elif isinstance(value, str):
            return unicode(value, 'utf-8')
        elif isinstance(value, datetime) or isinstance(value, date):
            return value.isoformat()
            """ 
        elif isinstance(value, BlobWrapper):
            return value.getFilename() 
            """
        elif isinstance(value, RichTextValue):
            return value.raw
        elif isinstance(value, RelationValue):
            relation = {}
            relation["from_id"] = value.from_id
            relation["from_path"] = value.from_path
            relation["to_id"] = value.to_id
            relation["to_path"] = value.to_path
            return relation
        elif isinstance(value, DateTime):
            # Zope DateTime
            # https://pypi.python.org/pypi/DateTime/3.0.2
            return value.ISO8601()
        elif hasattr(value, "isBinary") and value.isBinary("data"):
            # import pdb; pdb.set_trace()
            if not EXPORT_BINARY:
                return None

            # Archetypes FileField and ImageField payloads
            # are binary as OFS.Image.File object
            data = getattr(value.data, "data", None)
            if not data:
                return None
            return base64.b64encode(data)
        else:
            # Passthrough
            return value

    def grabArchetypesData(self, obj):
        """
        Export Archetypes schemad data as dictionary object.

        Binary fields are encoded as BASE64.
        """
        data = {}
        for field in obj.Schema().fields():
            name = field.getName()
            value = field.getRaw(obj)
            data[name] = self.convert(value)
        return data

    def grabDexterityData(self, obj):
        """
        Export Dexterity schemad data as dictionary object.
        Snippets taken from
        https://www.andreas-jung.com/contents
        """
        data = {}

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
            value = getattr(source_adapted, field.getName())
            data[name] = self.convert(value)
        return data

    def grabAttributes(self, obj):
        data = {}
        for key in EXPORT_ATTRIBUTES:
            data[key] = self.convert(getattr(obj, key, None))
        return data

    def export(self, folder, recursive=False):
        """
        Export content items.

        Possible to do recursively nesting into the children.

        :return: list of dictionaries
        """

        from plone.dexterity.content import Container
        from plone.dexterity.content import Item
        array = []
        for obj in folder.listFolderContents():
            # import pdb; pdb.set_trace()
            if isinstance(obj,Container) or isinstance(obj, Item):
                data = self.grabDexterityData(obj)
            else:
                data = self.grabArchetypesData(obj)
            data.update(self.grabAttributes(obj))

            if recursive:
                if IFolderish.providedBy(obj):
                    data["children"] = self.export(obj, True)

            array.append(data)

        return array

    def __call__(self):
        """
        """
        folder = self.context.aq_inner
        data = self.export(folder)
        pretty = json.dumps(data, sort_keys=True, indent=4)
        self.request.response.setHeader("Content-type", "application/json")
        return pretty


def spoof_request(app):
    """
    http://docs.plone.org/develop/plone/misc/commandline.html
    """
    from AccessControl.SecurityManagement import newSecurityManager
    from AccessControl.SecurityManager import setSecurityPolicy
    from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
    _policy = PermissiveSecurityPolicy()
    setSecurityPolicy(_policy)
    newSecurityManager(None, OmnipotentUser().__of__(app.acl_users))
    return app


def run_export_as_script(path):
    """ Command line helper function.

    Using from the command line::

        bin/instance script export.py yoursiteid/path/to/folder

    If you have a lot of binary data (images) you probably want

        bin/instance script export.py yoursiteid/path/to/folder > yourdata.json

    ... to prevent your terminal being flooded with base64.

    Or just pure data, no binary::

        EXPORT_BINARY=false bin/instance run export.py yoursiteid/path/to/folder

    :param path: Full ZODB path to the folder
    """
    global app

    secure_aware_app = spoof_request(app)
    folder = secure_aware_app.unrestrictedTraverse(path)
    view = ExportFolderAsJSON(folder, None)
    data = view.export(folder, recursive=True)
    # Pretty pony is prettttyyyyy
    pretty = json.dumps(data, sort_keys=True, indent=4)
    print pretty


# Detect if run as a bin/instance run script
if "app" in globals():
    run_export_as_script(sys.argv[3])
