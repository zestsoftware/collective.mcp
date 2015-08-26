from Testing import ZopeTestCase as ztc
import doctest
import unittest

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
