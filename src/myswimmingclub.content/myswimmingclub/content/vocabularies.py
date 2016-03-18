from myswimmingclub.content import MessageFactory as _

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from myswimmingclub.content.interfaces import IMySwimmingClubSettings

class StrokesVocabularyFactory(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        strokes = []

        registry = queryUtility(IRegistry)

        if registry is None:
            return SimpleVocabulary.fromItems(strokes)

        settings = registry.forInterface(IMySwimmingClubSettings, check=False)

        if settings.swimmingEvents is None:
            return SimpleVocabulary.fromItems(strokes)

        for nvp in [ e.split(u'|') for e in settings.swimmingEvents ]:
             v = t = nvp[0]
             t = (len(nvp) ==  1) and nvp[0] or nvp[1]
             strokes.append(SimpleTerm(value=v, title=t))

        return SimpleVocabulary(strokes)

StrokesVocabularyFactory = StrokesVocabularyFactory()

