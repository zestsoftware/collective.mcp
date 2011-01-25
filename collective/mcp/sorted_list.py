import logging
logger = logging.getLogger('collective.mcp')

class SortableObj(object):
    """ That class is only here for testing purpose.
    """
    def __init__(self, obj_id, before=None, after=None):
        self.id = obj_id
        self.before = before
        self.after = after

    def __repr__(self):
        return '<Sortable object: %s>' % self.id
    
class SortedList(list):
    """ This type of list adds a 'add' method, that will insert
    the object at the correct position, based on 'before'/'after'
    attributes of the object.
    """
    def __init__(self, *args, **kwargs):
        if 'id_attr' in kwargs:
            id_attribute = kwargs['id_attr']
            del kwargs['id_attr']
        else:
            id_attribute = 'id'
        super(SortedList, self).__init__(*args, **kwargs)
        self.id_attribute = id_attribute

    def add(self, obj):
        """ This method adds an object to the list and  will place it according
        to the 'before'/'after' attribute.

        If the object do not specify a position, it is
        appended to the list.
        >>> l = SortedList()
        >>> l.add(SortableObj('bla'))
        >>> l
        [<Sortable object: bla>]

        >>> l.add(SortableObj('bli'))
        >>> l
        [<Sortable object: bla>, <Sortable object: bli>]

        If an object just specify the 'after' property,
        it will be placed just after the object asked.
        >>> l.add(SortableObj('blu',
        ...                   after='bla'))
        >>> l
        [<Sortable object: bla>, <Sortable object: blu>, <Sortable object: bli>]

        Same thing for the 'before' property
        >>> l.add(SortableObj('blo',
        ...                   before='blu'))
        >>> l
        [<Sortable object: bla>, <Sortable object: blo>, <Sortable object: blu>,
         <Sortable object: bli>]

        And of course, it it specifies both, we
        will try to place it in between.
        >>> l.add(SortableObj('ble',
        ...                   before='bli',
        ...                   after='blu'))
        >>> l
        [<Sortable object: bla>, <Sortable object: blo>, <Sortable object: blu>,
         <Sortable object: ble>, <Sortable object: bli>]

        If existing objects are specifying unknown relation, they
        will be taken into account.
        >>> l.add(SortableObj('after_a',
        ...                   after='a'))
        >>> l
        [<Sortable object: bla>, <Sortable object: blo>, <Sortable object: blu>,
         <Sortable object: ble>, <Sortable object: bli>, <Sortable object: after_a>]
        >>> l.add(SortableObj('a'))
        >>> l
        [<Sortable object: bla>, <Sortable object: blo>, <Sortable object: blu>,
         <Sortable object: ble>, <Sortable object: bli>, <Sortable object: a>,
         <Sortable object: after_a>]

        If needed, the objects in the list can also be re-positionned.
        >>> l1 = SortedList()
        >>> l1.add(SortableObj('c', after='b'))
        >>> l1.add(SortableObj('a', before='b'))
        >>> l1
        [<Sortable object: c>, <Sortable object: a>]
        >>> l1.add(SortableObj('b'))
        >>> l1
        [<Sortable object: a>, <Sortable object: b>, <Sortable object: c>]
        """
        try:
            obj_id = getattr(obj, self.id_attribute)
        except AttributeError:
            return

        after_position = None
        before_position = None
        
        for index, o in enumerate(self):
            o_id = getattr(o, self.id_attribute)

            # We always increment after_position
            # as long as we find a reason to continue
            if o.before == obj_id or \
               obj.after == o_id:
                after_position = index + 1

            # Once a before_position has been found, it is
            # never changed (which is logical)
            if before_position is None and \
               (o.after == obj_id or \
                obj.before == o_id):
                before_position = index

        if after_position is None and \
           before_position is None:
            # Well, we don't really have a clue about what to do, let's
            # put it at the end.
            self.append(obj)

        elif after_position is None and \
             before_position is not None:
            # We place it just before the asked position.
            self.insert(before_position, obj)

        elif before_position is None and \
            after_position is not None:
            # Ok, we place it just after the position we found.
            self.insert(after_position, obj)

        elif after_position <= before_position:
            # Logically, if we arrived here, both objects
            # are not None.
            # This case is the "classic" case, the object has to
            # be placed between two elements.
            self.insert(after_position, obj)

        else:
            # Ok, that case sucks, it means we need to reorganize
            # the list.

            # First, we check that there is no possible clash (typically,
            # the element must be before AND after another one)
            all_before = self.find_all_before([obj])
            all_after = self.find_all_after([obj])
            conflicts = [x for x in self
                         if x in all_before and x in all_after]
            if conflicts:
                msg = 'Could not place object %s, as those objects ' +\
                      'must be before ADN after it: %s'
                logger.warn(msg % (obj, conflicts))
                self.append(obj)
                return
            
            # Now what we will do is place objects in the 'all_before' list
            # just before the first element of 'all_after'.
            position = self.find_first_element(all_after)
            self.insert(position, obj)
            to_delete = []
            for o in sorted(all_before,
                            reverse=True,
                            key = lambda x: self.index(x)):
                self.remove(o)
                self.insert(position, o)

    def _find_all(self, objects, match):
        """  
        """
        path = objects
        found = []

        while path:
            current = path.pop(0)
            for o in self:
                if o == current:
                    # We'll try to avoid recursion.
                    continue

                if match(current, o) and \
                   not o in found:
                    found.append(o)
                    path.append(o)

        return found

    def find_all_before(self, objects):
        """ Finds every objects that are supposed to be
        placed before any objects in the list.

        It finds direct relations (here 'a' and 'b'
        explicitely say that they are before 'c')
        >>> l = SortedList()
        >>> l.add(SortableObj('a', before = 'c'))
        >>> l.add(SortableObj('b', before = 'c'))
        >>> l.add(SortableObj('c', before = 'd'))
        >>> l
        [<Sortable object: a>, <Sortable object: b>, <Sortable object: c>]
        >>> l.find_all_before([l[2]])
        [<Sortable object: a>, <Sortable object: b>]

        And also indirect ones ('a' and 'b' appears
        as they are before 'c' who is before 'd')
        >>> l.add(SortableObj('d'))
        >>> l.find_all_before([l[-1]])
        [<Sortable object: c>, <Sortable object: a>, <Sortable object: b>]

        And if nothing can be found, well if returns an empty list.
        >>> l.find_all_before([l[0]])
        []
        """
        def compare(current, o):
            current_id = getattr(current, self.id_attribute)
            o_id = getattr(o, self.id_attribute)

            return o.before == current_id or \
                   current.after == o_id
            
        return self._find_all(objects, compare)

    def find_all_after(self, objects):
        """ Same principle as 'find_add_before', except
        if seeks for all objects that are supposed to be placed
        after any object in the objects list.

        It finds direct relations (here 'b' and 'c'
        explicitely say that they are before 'a')
        >>> l = SortedList()
        >>> l.add(SortableObj('c', after = 'a'))
        >>> l.add(SortableObj('b', after = 'a'))
        >>> l.add(SortableObj('a', after = '0'))
        >>> l
        [<Sortable object: a>, <Sortable object: c>, <Sortable object: b>]
        >>> l.find_all_after([l[0]])
        [<Sortable object: c>, <Sortable object: b>]

        And also indirect ones ('b' and 'c' appears
        as they are after 'a' who is after '0')
        >>> l.add(SortableObj('0'))
        >>> l.find_all_after([l[0]])
        [<Sortable object: a>, <Sortable object: c>, <Sortable object: b>]

        >>> l.find_all_after([l[-1]])
        []
        """
        def compare(current, o):
            current_id = getattr(current, self.id_attribute)
            o_id = getattr(o, self.id_attribute)

            return o.after == current_id or \
                   current.before == o_id
            
        return self._find_all(objects, compare)

    def find_first_element(self, objects):
        """ Finds the position of the first
        element listed in objects.

        >>> l = SortedList()
        >>> l.add(SortableObj('a'))
        >>> l.add(SortableObj('b'))
        >>> l.add(SortableObj('c'))
        >>> l.add(SortableObj('d'))
        >>> l.add(SortableObj('e'))
        >>> l
        [<Sortable object: a>,
         <Sortable object: b>,
         <Sortable object: c>,
         <Sortable object: d>,
         <Sortable object: e>]

        >>> l.find_first_element([l[3], l[2], l[4]])
        2

        >>> l.find_first_element(['a', 'b', 'c'])
        """
        for index, obj in enumerate(self):
            if obj in objects:
                return index
