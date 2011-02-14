from collective.mcp import McpMessageFactory as _

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

    # A list of buttons that are appended after the default one.
    # Each button definition is a dictionnary with the following
    # keys:
    # - title: the string shown
    # - mode: the mode activated when clicking the button
    # - icon: the icon used the replace the title (not needed)
    multi_objects_extra_buttons = []

    # Before and after can be used to specify the position of the page in the
    # menu.
    # The value must correspond to the 'widget_id' attribute of the page that
    # is used for ordering.
    before = None
    after = None

    # You can define here lists of extra CSS/Javascript files for this page.
    extra_js = []
    extra_css = []

    @property
    def cancel_mode(self):
        if 'back' in self.modes:
            return 'back'
        return self.default_mode

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
        if objects and self.mode != 'add':
            return objects[0]['id']

        return None

    def make_link(self, mode, extra_params = None):
        """ Removes the unneeded '#widget_id' at the end of the link.
        """
        link = super(ControlPanelPage, self).make_link(mode, extra_params)
        return link.replace('#%s' % self.widget_id, '')
