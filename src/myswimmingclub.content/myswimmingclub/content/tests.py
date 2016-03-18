import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import myswimmingclub.content

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['myswimmingclub.content'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              myswimmingclub.content)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='myswimmingclub.content',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='myswimmingclub.content.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='myswimmingclub.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for SwimmingFolder
        ztc.ZopeDocFileSuite(
            'SwimmingFolder.txt',
            package='myswimmingclub.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for SwimmingMeetEvent
        ztc.ZopeDocFileSuite(
            'SwimmingMeetEvent.txt',
            package='myswimmingclub.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for PoolLocation
        ztc.ZopeDocFileSuite(
            'PoolLocation.txt',
            package='myswimmingclub.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for SwimmingMeet
        ztc.ZopeDocFileSuite(
            'SwimmingMeet.txt',
            package='myswimmingclub.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Swimmer
        ztc.ZopeDocFileSuite(
            'Swimmer.txt',
            package='myswimmingclub.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Squad
        ztc.ZopeDocFileSuite(
            'Squad.txt',
            package='myswimmingclub.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
