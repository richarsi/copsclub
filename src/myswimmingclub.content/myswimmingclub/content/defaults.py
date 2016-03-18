from myswimmingclub.content import MessageFactory as _

from zope.interface import implements
from plone.supermodel.interfaces import IDefaultFactory
from zope.schema.interfaces import IContextAwareDefaultFactory
# imports to read the registry
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from myswimmingclub.content.interfaces import IMySwimmingClubSettings

class DefaultStrokesFactory(object):
    implements(IDefaultFactory)

    def __call__(self):
        strokes = []

        registry = queryUtility(IRegistry)

        if registry is None:
            return strokes

        settings = registry.forInterface(IMySwimmingClubSettings, check=False)

        if settings.swimmingEvents is None:
            return strokes

        for nvp in [ e.split(u'|') for e in settings.swimmingEvents ]:
             v =  nvp[0]
             strokes.append({ 'stroke': v, 'notes': u''})

        return strokes

DefaultStrokesFactory = DefaultStrokesFactory()
