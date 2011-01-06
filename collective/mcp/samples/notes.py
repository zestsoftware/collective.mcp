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
        return self.context.restrictedTraverse('@@multimodeview_notes_sample')

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

    def _process_edit_form(self):
        self.notes_view.edit_note(
            self._get_note_id(),
            self.request.form.get('title'))

    def _process_delete_form(self):
        self.notes_view.delete_note(self._get_note_id())
        self.request.form['obj_id'] = None
