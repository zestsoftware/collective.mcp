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

def custom_sort(l, id_attr):
    """ Custom sort method to work with before/after
    attributes.
    id_attr is the name of the attribute referred by before/after.
    """
    # We first build a dictionnary to easily access the objects.
    obj_dict = dict(
        [(getattr(o, id_attr), o) for o in l])

    # For each object, we had two attributes _after and _before,
    # that contain the list of objects that are before and after them.
    # The trick here is if we declare the object A as being before object
    # B, A will appear in the _after atributes of B and B will appear in
    # the _before attribute of A.
    for o in l:
        o._after = []
        o._before = []

    # We now fill the _after and _before attributes.
    for o in l:
        if o.before in obj_dict:
            o._after.append(obj_dict[o.before])
            obj_dict[o.before]._before.append(o)

        if o.after in obj_dict:
            o._before.append(obj_dict[o.after])
            obj_dict[o.after]._after.append(o)

    # We get all object that do not follow any other category.
    roots = [o for o in l if not o._before]

    sorted_objs = []
    for o in roots:
        path = [o]

        while path:
            current = path.pop(0)
            path = getattr(current, '_after', []) + path
            sorted_objs.append(current)

    return sorted_objs

def sorted_categories():
    return custom_sort(categories, 'id')

def register_page(p):
    pages.append(p)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

