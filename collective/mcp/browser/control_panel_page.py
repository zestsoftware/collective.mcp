from collective.multimodeview.browser import MultiModeViewlet

class ControlPanelPage(MultiModeViewlet):
    # The category the page belongs to.
    category = ''

    # Relative URL of the icon shown in the main menu.
    icon = ''

    # Name declared in the ZCML
    zcml_id = ''

    # Tells if a page manages multiple objects.
    # In this case you need to define list_objects
    multi_objects = False

    # The mode used when clicking on an object
    # in the object list.
    multi_objects_default_mode = 'edit'

    # The default buttons displayed at the bottom
    # of the object list.
    # To use them, you need to have a 'add' and
    # 'delete' mode.
    multi_objects_buttons = ['add', 'delete']

    def __call__(self):
        self.on_call()
        return self.index()

    def list_objects(self):
        """ Returns a list of dictionnaries.
        Dictionnaries must have two keys:
         - id: which is the object id (at least
           something you can use to fetch id, it
           can be UID or anything else)
         - title: which is what is displayed
           in the left column.
        """
        return []

    def current_object_id(self):
        """ Returns the id of the object currently
        manager or None.
        It first checks for a 'obj_id' paramter
        in the request.
        If not (which is the case when you open the page
        for the first time), it returns the id object
        of the first object.
        """
        form = self.request.form
        if form.get('obj_id', None):
            return form.get('obj_id')

        objects = self.list_objects()
        if objects:
            return objects[0]['id']

        return None

    def objects_extra_buttons(self):
        """ to be defined.
        """
        return []
