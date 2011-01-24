# This module shows examples of what NOT to do when creating pages.

from Products.Five import BrowserView
from collective.mcp.samples.home_message import HomeMessage

class WrongCatIdHomeMessage(HomeMessage):
    """ This subclass uses an incorrect id when specifying
    the category (setings instead of settings)
    """
    category = 'setings'
    zcml_id = 'collective_mcp_home_message_defect1'
    widget_id = 'collective_mcp_home_message_defect1'
    title = 'Home message (in wrong category)'

class ClashingWidgetIdHomeMessage(HomeMessage):
    """ This subclass is using the same ``widget_id`` than 
    HomeMessage.
    It will not be displayed in the control panel and a warning will
    be shown in the logs.
    """
    zcml_id = 'collective_mcp_home_message_defect2'
    title = 'Home message (defect due to widget_id clash)'

class NoWidgetIdPage(BrowserView):
    """ Do not try to create a page that do not subclass
    collective.mcp.browser.control_panel_page.ControlPanelPage, you might
    miss important stuff, like the widget_id for example.
    """
    category = 'settings'
    zcml_id = 'collective_mcp_home_message_defect3'
    title = 'Home message (without widget_id)'
