from collective.multimodeview.browser import MultiModeViewlet

class ControlPanelPage(MultiModeViewlet):
    # The category the page belongs to.
    category = ''

    # Relative URL of the icon shown in the main menu.
    icon = ''

    # Name declared in the ZCML
    zcml_id = ''

    def __call__(self):
        self.on_call()
        return self.index()
