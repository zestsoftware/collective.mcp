import unittest
import doctest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

import transaction
from Products.Five import fiveconfigure, zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import collective.mcp
import collective.multimodeview

from collective.mcp.sorted_list import SortedList

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class TestCase(ptc.PloneTestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        
        from Products.Five.testbrowser import Browser
        self.browser = Browser()

    def login_as_user(self, username, password):
        self.browser.open('http://nohost/plone/logout')
        self.browser.open('http://nohost/plone/login_form')
        self.browser.getControl(name='__ac_name').value = username
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()

    def login_as_manager(self):
        self.login_as_user(
            ptc.portal_owner,
            ptc.default_password)
    
    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.multimodeview)
            ztc.installPackage(collective.multimodeview)

            zcml.load_config('configure.zcml',
                             collective.mcp)
            zcml.load_config('samples.zcml',
                             collective.mcp)
            ztc.installPackage(collective.mcp)

            # We need to clean what has been added by samples.
            collective.mcp.categories = SortedList(id_attr='id')
            collective.mcp.pages = SortedList(id_attr='widget_id')

            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def afterSetUp(self):
        # his hack allows us to get the traceback when the getting a
        # 500 error when using the browser.
        self.portal.error_log._ignored_exceptions = ()
        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising
        transaction.commit()

def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            '../../README.rst',
            package='collective.mcp',
            optionflags=OPTIONFLAGS,
            test_class=TestCase),
        ztc.FunctionalDocFileSuite(
            'doc/restriction.rst',
            package='collective.mcp',
            optionflags=OPTIONFLAGS,
            test_class=TestCase),
        ztc.FunctionalDocFileSuite(
            'doc/defect.rst',
            package='collective.mcp',
            optionflags=OPTIONFLAGS,
            test_class=TestCase),
        ztc.FunctionalDocFileSuite(
            'doc/modes.rst',
            package='collective.mcp',
            optionflags=OPTIONFLAGS,
            test_class=TestCase),
        ztc.FunctionalDocFileSuite(
            'doc/multiobjects.rst',
            package='collective.mcp',
            optionflags=OPTIONFLAGS,
            test_class=TestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
