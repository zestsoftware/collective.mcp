from collective.mcp.category import Category
from collective.mcp.sorted_list import SortedList
from zope.i18nmessageid import MessageFactory
import logging

logger = logging.getLogger('collective.mcp')
McpMessageFactory = MessageFactory(u'collective.mcp')

categories = SortedList(id_attr='id')
pages = SortedList(id_attr='widget_id')


def register_category(cat):
    if isinstance(cat, Category):
        if cat.id in [c.id for c in categories]:
            logger.info('Category id "%s" already exists' % cat.id)
        else:
            categories.add(cat)
    else:
        raise TypeError('Expected Category object, found %s' % type(cat))


def register_page(p):
    if p.category not in categories:
        logger.info('There is no "%s" category registered' % p.category)
    pages.add(p)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
