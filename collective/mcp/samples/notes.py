from collective.mcp.browser.control_panel_page import ControlPanelPage

class Notes(ControlPanelPage):
    category = 'settings'
    zcml_id = 'collective_mcp_notes'
    widget_id = 'collective_mcp_notes'
    icon = "++resource++collective_mcp_notes.png"
    title = 'Notes'

    modes = {'add': {'success_msg': 'The note has been added',
                     'error_msg': 'Impossible to add a note: please correct the form',
                     'submit_label': 'Add note'},
             'edit': {'success_msg': 'The note has been edited',
                     'submit_label': 'Edit note'},
             'delete': {'success_msg': 'The note has been deleted',
                        'submit_label': 'Delete note'}
             }
    default_mode = 'edit'
    multi_objects = True

    @property
    def notes_view(self):
        return self.context.restrictedTraverse('@@mcp_multimodeview_notes_sample')

    def list_objects(self):
        notes = self.notes_view.get_notes()

        return [{'id': note_id, 'title': note_text}
                for note_id, note_text in enumerate(notes)
                if note_text]

    def _get_note_id(self):
        notes = self.notes_view.get_notes()
        note_id = self.current_object_id()

        try:
            note_id = int(note_id)
        except:
            # This should not happen, something wrong happened
            # with the form.
            return

        if note_id < 0 or note_id >= len(notes):
            # Again, something wrong hapenned.
            return

        if notes[note_id] is None:
            # This note has been deleted, nothing should be done
            # with it.
            return

        return note_id

    def get_note_title(self):
        """ Returns the title of the note currently edited.
        """
        if self.errors:
            return self.request.form.get('title')

        if self.is_add_mode:
            return ''

        note_id = self._get_note_id()
        if note_id is None:
            # This should not happen.
            return ''

        return self.notes_view.get_notes()[note_id]

    def _check_add_form(self):
        if not self.request.form.get('title'):
            self.errors['title'] = 'You must provide a title'

        return True

    def _check_edit_form(self):
        if self._get_note_id() is None:
            return

        return self._check_add_form()

    def _check_delete_form(self):
        return self._get_note_id() is not None

    def _process_add_form(self):
        self.notes_view.add_note(self.request.form.get('title'))
        self.request.form['obj_id'] = len(self.notes_view.get_notes()) - 1

    def _process_edit_form(self):
        self.notes_view.edit_note(
            self._get_note_id(),
            self.request.form.get('title'))

    def _process_delete_form(self):
        self.notes_view.delete_note(self._get_note_id())
        self.request.form['obj_id'] = None

class NotesDisplay(Notes):
    """ More or less the same than the previous one, except it
    has an extra 'display' mode.
    """
    zcml_id = 'collective_mcp_notes_display'
    widget_id = 'collective_mcp_notes_display'
    title = 'Displayed notes'

    modes = {'add': {'success_msg': 'The note has been added',
                     'error_msg': 'Impossible to add a note: please correct the form',
                     'submit_label': 'Add note'},
             'edit': {'success_msg': 'The note has been edited',
                     'submit_label': 'Edit note'},
             'display': {'success_msg': 'Display zones for the note have been updated',
                         'submit_label': 'Set display zones'},
             'delete': {'success_msg': 'The note has been deleted',
                        'submit_label': 'Delete note'}
             }

    multi_objects_extra_buttons = [
        {'mode': 'display',
         'title': 'Change display zones',
         'icon': '++resource++display_button.png'}]

    def get_zones(self):
        zones = []

        note_id = self._get_note_id()
        display_zones = self.notes_view.get_display_zones()
        note_display_zones = display_zones.get(note_id, [])

        for zone in self.notes_view.display_zones_list:
            zones.append({'value': zone,
                          'checked': zone in note_display_zones})
        return zones

    def _check_display_form(self):
	  return True

    def _process_display_form(self):
        zones = self.request.form.get('zones', [])

        if isinstance(zones, str):
            # Only one zone has been checked.
            zones = [zones]

        self.notes_view.set_display_zones(
            self._get_note_id(),
            zones)

class NotesDisplayModeSwitch(NotesDisplay):
    """ Same principle than the previous one.
    It adds some extra parameters when defining the mode to declare
    to which mode switch after adding a note or after cancelling.
    """
    zcml_id = 'collective_mcp_notes_mode_switch'
    widget_id = 'collective_mcp_notes_mode_switch'
    title = 'Mode switching notes'

    modes = {'add': {'success_msg': 'The note has been added',
                     'error_msg': 'Impossible to add a note: please correct the form',
                     'submit_label': 'Add note',
                     'cancel_mode': 'add',
                     'success_mode': 'display'},
             'edit': {'success_msg': 'The note has been edited',
                     'submit_label': 'Edit note'},
             'display': {'success_msg': 'Display zones for the note have been updated',
                         'submit_label': 'Set display zones'},
             'delete': {'success_msg': 'The note has been deleted',
                        'submit_label': 'Delete note'}
             }
