Theming the control panel
=========================

The main structure of a control panel page is the following one::

<div#control_panel_container>
  <div#control_panel_header />
  <div#control_panel_content>
    <div#subpage />
    <div#objects_list />
    <ul.menu />
  </div>
</div>

The control_panel_container is the main div, containing all the
control panel.

The control_panel_header contains the breadcrumbs to navigate in the
control panel (well, go back home mainly, there's no more that 2
levels available)

The control_panel_content contains the rest of the control panel (the
menu or the page itself).

Control panel subpage
---------------------

The div#subpage has some default classes::

 - 'mcp_widget_XXX' where XXX is the widget id

 - 'right_column' is added when the page alows to edit multiple objects.

For example, the home message page does not allow editing multiple
objects, so it will only have the 'mcp_widget_home_message' class::

    >>> from collective.mcp.tests.utils import McpHtmlParser
    >>> parser =  McpHtmlParser()

    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> self.browser.getLink('Home message').click()
    >>> parser.feed(self.browser.contents)
    >>> parser.subpage_classes
    'mcp_widget_collective_mcp_home_message'

The page to edit the notes will have the right columns class::

    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> self.browser.getLink('Notes').click()
    >>> parser.feed(self.browser.contents)
    >>> parser.subpage_classes
    'mcp_widget_collective_mcp_notes right_column'


It is possible to add some custom classes here, by defining the
'sub_page_classes' attribute of the page.
For example::

    >>> from collective.mcp.samples.home_message import HomeMessage
    >>> HomeMessage.sub_page_classes = ['mcp_sample_home', 'another_custom_class']
    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> self.browser.getLink('Home message').click()
    >>> parser.feed(self.browser.contents)
    >>> parser.subpage_classes
    'mcp_sample_home another_custom_class mcp_widget_collective_mcp_home_message'
