from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('myswimmingclub.content') 

from plone.formwidget.contenttree.widget import ContentTreeFieldWidget
from plone.formwidget.contenttree.widget import MultiContentTreeFieldWidget

from plone.formwidget.contenttree.source import PathSourceBinder,\
    ObjPathSourceBinder, UUIDSourceBinder

from myswimmingclub.content.squad import ISquad
from myswimmingclub.content.pool_location import IPoolLocation

# Some binder instances for use with plone.supermodel schemas
path_src_binder = PathSourceBinder()
obj_path_src_binder = ObjPathSourceBinder()
uuid_src_binder = UUIDSourceBinder()
squad_path_src_binder = ObjPathSourceBinder(object_provides=ISquad.__identifier__)
pool_location_path_src_binder = ObjPathSourceBinder(object_provides=IPoolLocation.__identifier__)
