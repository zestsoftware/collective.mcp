from collective.mcp.browser.control_panel_page import ControlPanelPage

class HomeMessage(ControlPanelPage):
    category = 'settings'
    zcml_id = 'collective_mcp_home_message'
    widget_id = 'collective_mcp_home_message'
    icon = "++resource++collective_mcp_home.png"
    title = 'Home message'

    modes = {'back': {},
             'default': {'submit_label': 'Update home message',
                         'success_msg': 'The home message has been updated'}}
    default_mode = 'default'

    @property
    def notes_view(self):
        return self.context.restrictedTraverse('@@mcp_multimodeview_notes_sample')

    def _check_default_form(self):
        return True

    def _process_default_form(self):
        self.notes_view.set_home_message(
            self.request.form.get('msg', ''))
        return 'back'
    
