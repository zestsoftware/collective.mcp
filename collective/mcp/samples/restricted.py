# Customized versions of the pages defined in notes.py and home_message
# with restricted accesses.

from collective.mcp.samples.notes import Notes
from collective.mcp.samples.home_message import HomeMessage

class HomeMessageRestricted(HomeMessage):
    zcml_id = 'collective_mcp_home_message_restricted'
    widget_id = 'collective_mcp_home_message_restricted'
    title = 'Home message (restricted to admin)'

class HomeMessageRestrictedII(HomeMessage):
    zcml_id = 'collective_mcp_home_message_restrictedII'
    widget_id = 'collective_mcp_home_message_restrictedII'
    title = 'Home message (restricted using "permission" attribute)'

    view_permission = 'Manage portal'

class HomeMessageRestrictedIII(HomeMessage):
    zcml_id = 'collective_mcp_home_message_restrictedIII'
    widget_id = 'collective_mcp_home_message_restrictedIII'
    title = 'Home message (restricted using "is_shown" method)'

    def is_shown(self):
        """ Now the page is only visible is you are not a manager.
        Yes it's not a real-life use case.
        """
        user = self.get_user()
        if user:
            return 'Manager' not in user.getRolesInContext(
                self.context)
        return True

class NotesRestricted(Notes):
    zcml_id = 'collective_mcp_notes_restricted'
    widget_id = 'collective_mcp_notes_restricted'
    title = 'Partially restricted notes'

    @property
    def modes(self):
        modes = {'add': {'success_msg': 'The note has been added',
                         'error_msg': 'Impossible to add a note: please correct the form',
                         'submit_label': 'Add note'},
                 'edit': {'success_msg': 'The note has been edited',
                          'submit_label': 'Edit note'}}

        if self.check_permission('Manage portal'):
            modes['delete'] = {'success_msg': 'The note has been deleted',
                           'submit_label': 'Add note'}
        return modes

    @property
    def multi_objects_buttons(self):
        buttons = ['add']
        if self.check_permission('Manage portal'):
            buttons.append('delete')

        return buttons
