import logging 

from category import Category

logger = logging.getLogger('collective.mcp')

categories = []
pages = []

def register_category(cat):
    if isinstance(cat, Category):
        categories.append(cat)
    else:
        raise TypeError('Expected Category object, found %s' % type(cat))

def register_page(p):
    pages.append(p)
    # else:
    #     raise TypeError('Expected ControlPanelPage object, found %s' % type(p))

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

