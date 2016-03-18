import datetime
from DateTime import DateTime
import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from myswimmingclub.content.testing import MYSWIMMINGCLUB_CONTENT_INTEGRATION_TESTING

from zope.interface import Invalid
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.event import notify

from zope.schema.interfaces import IVocabularyFactory

from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.event import ObjectInitializedEvent

class TestContent(unittest.TestCase):

    layer = MYSWIMMINGCLUB_CONTENT_INTEGRATION_TESTING
    # set the dates that we're going to use in our tests
    today = datetime.date.today()
    days01 = datetime.timedelta(days=1)
    days02 = datetime.timedelta(days=2)
    days07 = datetime.timedelta(days=7)
    days08 = datetime.timedelta(days=8)  # organisers_entry_date
    days30 = datetime.timedelta(days=30) # start
    days31 = datetime.timedelta(days=31) # end
    days32 = datetime.timedelta(days=32) # age_as_of_date

    def test_hierarchy(self):
        portal = self.layer['portal']
        
        # Ensure that we can create the various content types without error
        # myswimmingclub.squad
        # myswimmingclub.swimmer
        # myswimmingclub.swimmingfolder
        # myswimmingclub.swimmingmeet
        # myswimmingclub.poollocation
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('myswimmingclub.squad', 
                                'sq1', title=u"Squad 1")
        portal.invokeFactory('myswimmingclub.swimmer', 
                                'sw1', title=u"Swimmer 1")
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'cf1', title=u"Cinema folder 1")
        portal['cf1'].invokeFactory('myswimmingclub.swimmingfolder', 
                                'cf2', title=u"Cinema folderi 2")
        portal['cf1'].invokeFactory('myswimmingclub.poollocation', 
                                'loc1', title=u"Location 1")
        portal['cf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm1', title=u"Swimming Meet 1")
        portal['cf1'].invokeFactory('Event', 
                                'e1', title=u"Event 1")
        
        setRoles(portal, TEST_USER_ID, ('Editor',))
        
        portal['cf1']['sm1'].invokeFactory('File', 
                                'f1', title=u"File 1")

    def test_swimmingmeet_start_index(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        

        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'cf1', title=u"Cinema folder 1")
        portal['cf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm1', title=u"Swimming Meet 1",
                                start=self.today + self.days30)

        sm1 = portal['cf1']['sm1']
        # sm1.reindexObject()

        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog({'start': self.today + self.days30 })

        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), sm1.absolute_url())

    def test_swimmingmeet_end_index(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'cf1', title=u"Cinema folder 1")
        portal['cf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm1', title=u"Swimming Meet 1",
                                end=self.today + self.days31)

        sm1 = portal['cf1']['sm1']

        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog({'end': self.today + self.days31 })

        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), sm1.absolute_url())

    def test_swimmingfolder_date_range_formatted(self):
        start = datetime.date(2013,12,30)
        same_day = datetime.date(2013,12,30)
        next_day = datetime.date(2013,12,31)
        next_month = datetime.date(2014,01,01)
        start_with_time = DateTime(2013,12,30,8,30)
        end_with_time = DateTime(2013,12,30,20,30)
        
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('myswimmingclub.swimmingfolder',
                                'sf1', title=u"Swimming folder 1")
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'sf2', title=u"Swimming folder 2")
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'sf3', title=u"Swimming folder 3")
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'sf4', title=u"Swimming folder 4")
        portal['sf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm1', title=u"Swimming Meet 1",
                                start=start,
                                end=same_day)
        portal['sf2'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm2', title=u"Swimming Meet 2",
                                start=start,
                                end=next_day)
        portal['sf3'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm3', title=u"Swimming Meet 3",
                                start=start,
                                end=next_month)
        portal['sf4'].invokeFactory('Event', 'ev1', title=u"Event 1",
                                startDate=start_with_time,
                                endDate=end_with_time)

        sf1 = portal['sf1']
        sf2 = portal['sf2']
        sf3 = portal['sf3']
        sf4 = portal['sf4']
        ev1 = portal['sf4']['ev1']
        ev1.reindexObject()

        view = sf1.restrictedTraverse('@@view')
        folder_contents = view.folder_contents()
        self.assertEqual(1, len(folder_contents))
        self.assertEqual(u"30 Dec 2013",
                          folder_contents[0]['date_range_formatted'])

        view = sf2.restrictedTraverse('@@view')
        folder_contents = view.folder_contents()
        self.assertEqual(1, len(folder_contents))
        self.assertEqual(u"30 - 31 Dec 2013",
                          folder_contents[0]['date_range_formatted'])

        view = sf3.restrictedTraverse('@@view')
        folder_contents = view.folder_contents()
        self.assertEqual(1, len(folder_contents))
        self.assertEqual(u"30 Dec - 01 Jan 2014",
                          folder_contents[0]['date_range_formatted'])

        view = sf4.restrictedTraverse('@@all-sf-content')
        folder_contents = view.folder_contents()
        self.assertEqual(1, len(folder_contents))
        self.assertEqual(u"30 Dec 2013",
                          folder_contents[0]['date_range_formatted'])

    def test_swimmingfolder_days_left(self):
        tomorrow = self.today + self.days01
        tomorrow_plus_1 = tomorrow + self.days01
        tomorrow_plus_2 = tomorrow_plus_1 + self.days01
        
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'sf1', title=u"Swimming folder 1")
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'sf2', title=u"Swimming folder 2")
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'sf3', title=u"Swimming folder 3")
        portal['sf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm1', title=u"Swimming Meet 1",
                                start=self.today,
                                club_entry_date=self.today,
                                organisers_entry_date=self.today)
        portal['sf2'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm2', title=u"Swimming Meet 2",
                                start=self.today,
                                club_entry_date=tomorrow_plus_1,
                                organisers_entry_date=tomorrow)
        portal['sf3'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm3', title=u"Swimming Meet 3",
                                start=self.today,
                                club_entry_date=tomorrow_plus_1,
                                organisers_entry_date=tomorrow_plus_2)

        sf1 = portal['sf1']
        sf2 = portal['sf2']
        sf3 = portal['sf3']

        view = sf1.restrictedTraverse('@@view')
        folder_contents = view.folder_contents()
        self.assertEqual(1, len(folder_contents))
        self.assertEqual(0, folder_contents[0]['days_left'])
        self.assertEqual(u"Entry Closed",
                           folder_contents[0]['days_left_formatted'])

        view = sf2.restrictedTraverse('@@view')
        folder_contents = view.folder_contents()
        self.assertEqual(1, len(folder_contents))
        self.assertEqual(1, folder_contents[0]['days_left'])
        self.assertEqual(u"1 day left to enter",
                           folder_contents[0]['days_left_formatted'])

        view = sf3.restrictedTraverse('@@view')
        folder_contents = view.folder_contents()
        self.assertEqual(1, len(folder_contents))
        self.assertEqual(2, folder_contents[0]['days_left'])
        self.assertEqual(u"2 days left to enter",
                           folder_contents[0]['days_left_formatted'])

    def test_swimmingfolder_sort(self):
        yesterday = self.today - self.days01
        tomorrow = self.today + self.days01
        
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('myswimmingclub.swimmingfolder', 
                                'sf1', title=u"Swimming folder 1")
        portal['sf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm1', title=u"Swimming Meet 1",
                                start=self.today)
        portal['sf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm2', title=u"Swimming Meet 2",
                                start=tomorrow)
        portal['sf1'].invokeFactory('myswimmingclub.swimmingmeet', 
                                'sm3', title=u"Swimming Meet 3",
                                start=yesterday)


        sf1 = portal['sf1']

        view = sf1.restrictedTraverse('@@view')
        folder_contents = view.folder_contents()
        self.assertEqual(3, len(folder_contents))
        self.assertEqual(u"Swimming Meet 3", 
                          folder_contents[0]['title'])
        self.assertEqual(u"Swimming Meet 1", 
                          folder_contents[1]['title'])
        self.assertEqual(u"Swimming Meet 2", 
                          folder_contents[2]['title'])

