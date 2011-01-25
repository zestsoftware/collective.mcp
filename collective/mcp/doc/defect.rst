Some errors to avoid
====================

This doc shows some examples of errors you might fall into when
creating your custom pages for the control panel (and also test that
the system handles correctly those problems).

The source code can be found in ``collective/mcp/samples/defect.py``.

Registering non ``Category`` objects
------------------------------------

When registering categories, you have to use the ``Category`` class
(that sounds logic)::

    >>> from collective.mcp import Category, register_category, categories
    >>> categories
    [Category: personal,
     Category: settings]

    >>> register_category(
    ...     Category('my_category',
    ...              'Ho, that is a real category'))
    >>> categories
    [Category: personal,
     Category: settings,
     Category: my_category]

Or a sub-class of Categorie works too. For example, you might want to
override the ``__repr__`` method. In most cases, you might want to
override the ``getTitle`` method to have a dymanic name for the category::

    >>> class Categorie(Category):
    ...     def __repr__(self):
    ...         return 'Categorie, a french one: %s' % self.id

    >>> register_category(
    ...     Categorie('french_cat',
    ...               'Je suis une categorie'))
    >>> categories
    [Category: personal,
     Category: settings,
     Category: my_category,
     Categorie, a french one: french_cat]

But when you declare your custom type, do not forget to sub-class the
``Category`` class. In the other case, the system will not allow the registration::

    >>> class CustomCategory(object):
    ...     def __init__(self, cat_id, title):
    ...         self.cat_id = cat_id
    ...         self.title = title
    ...         self.before = None
    ...         self.after = None

    >>> register_category(
    ...     CustomCategory('customized',
    ...                    'I do not subclass Category and I do not care'))
    Traceback (most recent call last):
    ...
    TypeError: Expected Category object, found <class 'CustomCategory'>


Clashes with another category
-----------------------------

If you plan to integrate some pages for ``collective.mcp`` in a
product, it might be a good idea to prefix the ``ids`` of the
categories to avoid clashes.

By default, if you try to register a new category with an id that has
been already declared, the system will ignore it.

    >>> register_category(
    ...     Category('my_category',
    ...              'This is a category with an id clash'))
    >>> categories
    [Category: personal,
     Category: settings,
     Category: my_category,
     Categorie, a french one: french_cat]

Registering a page that do not match any category
-------------------------------------------------

When you create a page for the control panel, you have to specify the
``category`` attribute, so the system knows where to display the icon
on the control panel home page.

If you use a category id that do not exist, your page will not be
visible. Here, we defined a sub-class for the ``Home message`` page
(see README) using ``setings`` instead of ``settings`` as a category id::

  class WrongCatIdHomeMessage(HomeMessage):
      """ This subclass uses an incorrect id when specifying
      the category (setings instead of settings)
      """
      category = 'setings'
      zcml_id = 'collective_mcp_home_message_defect1'
      widget_id = 'collective_mcp_home_message_defect1'
      title = 'Home message (in wrong category)'

We register the page but it will not be shown in the control panel
home::

    >>> from collective.mcp import register_page
    >>> from collective.mcp.samples import WrongCatIdHomeMessage
    >>> register_page(WrongCatIdHomeMessage)

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> 'Home message (in wrong category)' in self.browser.contents
    False

When this happens, you will get a message 'There is no "setings"
category registered' in the logs (of course "setings is replaced by
your own mistake).

Registering a page with an already existing widget id
-----------------------------------------------------

Like for categories, the ``widget_id`` must be unique. So if you
register a page with a ``widget_id`` already in use, you'll get a
message in the logs and your page will not be shown.

  class ClashingWidgetIdHomeMessage(HomeMessage):
      """ This subclass is using the same ``widget_id`` than 
      HomeMessage.
      It will not be displayed in the control panel and a warning will
      be shown in the logs.
      """
      zcml_id = 'collective_mcp_home_message_defect2'
      title = 'Home message (defect due to widget_id clash)'

We register it and once again, it is not shown::

    >>> from collective.mcp import register_page
    >>> from collective.mcp.samples import ClashingWidgetIdHomeMessage
    >>> register_page(ClashingWidgetIdHomeMessage)

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> 'Home message (defect due to widget_id clash)' in self.browser.contents
    False

The message you get in the logs is: "widget_id '%s' is already
used. Choose another one."

Not sub-classing ControlPanelPage when creating your pages
----------------------------------------------------------

You might be tempted to create your own class for your pages without
subclassing
``collective.mcp.browser.control_panel_page.ControlPanelPage``. Well,
don't, that's not the most clever idea you had.

The problem when doing so it that you might miss important
methods/attributes declaration that will lead to errors.

Here we defined our own page that do not specify a ``widget_id`` attribute::

  class NoWidgetIdPage(BrowserView):
      """ Do not try to create a page that do not subclass
      collective.mcp.browser.control_panel_page.ControlPanelPage, you might
      miss important stuff, like the widget_id for example.
      """
      category = 'settings'
      zcml_id = 'collective_mcp_home_message_defect3'
      title = 'Home message (without widget_id)'

Once again, it is not shown in the control panel page (but no error is
raised hopefully - other missing attributes might lead to the well-known
"We're sorry but there's been an error" page)::

    >>> from collective.mcp import register_page
    >>> from collective.mcp.samples import NoWidgetIdPage
    >>> register_page(NoWidgetIdPage)

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> 'Home message (without widget_id)' in self.browser.contents
    False

    >>> '<span class="spacer">Settings</span>' in self.browser.contents
    True

Note: for the Category, we raise an error when registering a category
that is not a Category instance. For the pages, we can not do it as
Zope does some magic and even normal page are not instances of
ControlPanelPage.
If you know a way to solve the problem, do not hesitate.