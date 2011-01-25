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

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'tests/coverage.txt',
            package='collective.mcp',
            optionflags=OPTIONFLAGS),
        ztc.ZopeDocFileSuite(
            'tests/sorted_list.txt',
            package='collective.mcp',
            optionflags=OPTIONFLAGS),
        doctest.DocTestSuite(
            module='collective.mcp.sorted_list',
            optionflags=OPTIONFLAGS),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
