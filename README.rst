Introduction
============

collective.mcp is a Plone product that helps creating a custom control
panel for the site's users.
mcp stands for Mac Control Panel, as the base theme is inspired by the
Mac OSX control panel.

The goal is not to replace Plone's control panel but to help creating
a new one decidated to the users. This will might be usefull for web
applications based on Plone.

You can see some screenshots of the product at this page:
https://github.com/vincent-psarga/collective.mcp/wiki/Screenshots

This product does not magically create the pages for your site, it
only provides some API to create them, as we'll see later in this
README.

Installing collective.mcp
=========================

In your buildout, add collective.mcp in the eggs directory. Run
buildout, start your instance again and add the product using the
quick_installer (or the Plone equivqlent).
You can now access the control panel by accessing
``http://localhost:8080/your_plone_site/control_panel``. As you have
not added any page yet, you will get a message telling you that you
can not manage anything.

    >>> from collective.mcp import categories, pages
    >>> categories
    []
    >>> pages
    []


Viewing samples
===============

You can load the file ``samples.zcml`` file from collective.mcp to get
some samples.
For example, in the ``configure.zcml`` file of your theme::

  <include package="collective.mcp"
           file="samples.zcml" />

Restart the instance, reload the control panel page and you should see
some pages ready to be used.

Implementing your control panel
===============================

collective.mcp provides a place for the control panel, that you can
find at http://localhost:8080/ourplonesite/control_panel/.
Normally, the page will tell you "There is nothing you can manage.",
as you did not add any page yet.

To simplify, we'll consider that you already have a Plone product for
which you want to add a control panel. This one has a 'browser'
package. Inside the browser package, create a 'control_panel' package,
containing __init__.py and configure.zcml.

The __init__.py file you look like this (except you replace the
message factory by your own product message factory)::

    >>> from collective.mcp import Category, register_category, register_page
    >>> from collective.mcp import McpMessageFactory as _

And the configure.zcml file like this::

  <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser"
      xmlns:five="http://namespaces.zope.org/five"
      xmlns:i18n="http://namespaces.zope.org/i18n"
      i18n_domain="your_product">
  </configure>

In the configure.zcml file of the browser package, include your new
package::

  <include package=".control_panel" />

Now you have the base, we can start adding thing to the control panel.

Creating categories
-------------------

The first step is to create the categories to which the pages will
belong. If you have a look at the screenshots in the docs folder or on
the project wiki, there is four categories:

 - personal preferences

 - clients

 - templates

 - settings

In our example, we'll only create the first and last categories. To do
so, in the __init__.py, we'll add the following code::

    >>> register_category(
    ...     Category('personal',
    ...              _(u'label_cpcat_personal_prefs',
    ...                default=u'Personal preferences')))
    >>> register_category(
    ...     Category('settings',
    ...              _(u'label_cpcat_settings',
    ...                default=u'Settings'),
    ...              after='personal'))

As you can see, we specified that the 'settings' category will appear
after the 'personal' one. We could also have specified that 'personal'
is before 'settings' and get the same result.

If you reload now the control panel, nothing has changed. That is
normal, the system does not display categories for which there is no
page (or the user can not use any of the pages).

    >>> categories
    [Category: personal, Category: settings]
    >>> pages
    []

Creating a simple page
----------------------

collective.mcp is based on collective.multimodeview. For the pages,
we will rely on a view defined in the samples called
'multimodeview_notes_sample'. If you have already activated the
samples for multimodeview, you do not have to do anything.
In the other case, add the following lines to your configure.zcml
file:

  <browser:page
      for="*"
      name="multimodeview_notes_sample"
      class="collective.multimodeview.samples.notes_view.NotesView"
      permission="zope2.View"
      />

The first page we will create allows to update the 'home message',
using the API provded by the view declared above.
The API is pretty simple and do not realy need explanations:

- get_home_message()

- set_home_message(msg)

This message is not displayed anywhere. It could, but that's not
covered by this README.

To create our page, we'll first create a new python file in the
control panel package, called 'home_message.py', that contains the
following code::

  from collective.mcp.browser.control_panel_page import ControlPanelPage

  class HomeMessage(ControlPanelPage):
      category = 'settings'
      zcml_id = 'collective_mcp_home_message'
      widget_id = 'collective_mcp_home_message'

      modes = {'back': {},
               'default': {'submit_label': 'Update home message',
                           'success_msg': 'The home message has been updated'}}

      default_mode = 'default'

      @property
      def notes_view(self):
          return self.context.restrictedTraverse('@@multimodeview_notes_sample')

      def _check_default_form(self):
          return True

      def _process_default_form(self):
          self.notes_view.set_home_message(
              self.request.form.get('msg', ''))
          return 'back'

Let's have a look to what we defined::

 - 'category': this is the category to which our now page belongs

 - 'zmcl_id': this is the name of the page, as defined in the zcml
   file (we'll see it later)

 - 'widget_id': this is a unique identifier for your page. Here we
   used the same one that for the zcml_id ust to avoid any conflict,
   but it could have benn 'home_message' for example.

 - modes: this dictionnary defines the list of modes in which the page
   can be. We defined a 'back' mode, that means that when the form is
   submitted or when the user cancels, the home of the conrol panel
   will be shown instead of the form again. For the default mode, we
   also defined the name of the button to save and the message
   displayed on success. Have a look to collective.multimodeview
   README file to see more options you can define for modes.

 - notes_view: just a helper property to easily get the view with the
   API.

 - _check_default_form: a function that checks that the form submitted
   did not contain error. Here we do not check anything so it's prettu
   quick, the second example will show more. see
   colective.multimodeview for more explanation).

 - _process_default_form: the function called if no errors were found
   by the previous method. As you can guess by the name, it processes
   the form (here it updates the home message).

Now we need a template for our view::

  <form method="post"
        tal:attributes="action view/get_form_action">

    <div class="field">
      <label for="msg">Message:</label>
      <input type="text"
             name="msg"
             tal:attributes="value view/notes_view/get_home_message" />
    </div>
    <span tal:replace="structure view/make_form_extras" />
  </form>

There is nothing fancy here, except the use of two methods from
multimodeview::

 - view/get_form_action: gives the action for the form

 - view/make_form_extra: generates some HTML code with some hidden
   input fields and the submit buttons.

Once again, have a look to collective.multimodeview for more
explanations.

The last step is to declare our view in the zcml file and register
it. First, in the __init__.py file::

    >>> from collective.mcp.samples.home_message import HomeMessage
    >>> register_page(HomeMessage)

This makes the page appear in the ``pages`` list::

    >>> pages
    [<class 'collective.mcp.samples.home_message.HomeMessage'>]

Then in the ZCML file::

  <browser:page
      for="*"
      name="collective_mcp_home_message"
      class=".HomeMessage"
      permission="zope.Public"
      template="home_message.pt"
      />

Now you can restart the server and reload the control panel. The
'settings' category will appear, containing one page with a question
mark icon.

    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'There is nothing you can manage.' in self.browser.contents
    False

    >>> '<span class="spacer">Settings</span>' in self.browser.contents
    True

    >>> '<span class="spacer">Personal preferences</span>' in self.browser.contents
    False


First, let's solve the icon problem. In the sample directory you will
find two icons taken from this set:
http://www.iconfinder.com/search/?q=iconset%3A49handdrawing

Let's declare the home.png file in the zcml::

  <browser:resource
      name="collective_mcp_home.png"
      file="home.png" />

And now in our view, we will use this icon::

  class HomeMessage(ControlPanelPage):
      icon = "++resource++collective_mcp_home.png"

The second problem is that our page does not have a title, this
problem can easily be solved too::

  class HomeMessage(ControlPanelPage):
      title = 'Home message'

The image now appears in the control panel and the title is also displayed::

    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    True
    >>> '<span>Home message</span>' in self.browser.contents
    True

If we click on the icon, the main page is not displayed anymore and we
see our form instead::

    >>> self.browser.getLink('Home message').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=default&widget_id=collective_mcp_home_message'

    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    False
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    True

We can fill the home message and validate. We get a sucess message
displayed and we are back on the control panel home page::

    >>> self.browser.getControl(name='msg').value = 'My new home message - welcome :)'
    >>> self.browser.getControl(name='form_submitted').click()
    >>> "<dd>The home message has been updated</dd>" in self.browser.contents
    True

If we had cancelled, we would have got a different message (which is
the default cancel message inherited from collective.multimodeview) ::

    >>> self.browser.getLink('Home message').click()
    >>> self.browser.getControl(name='form_cancelled').click()
    >>> "<dd>Changes have been cancelled.</dd>" in self.browser.contents
    True

And that's all, you have your first page of the control panel
working. Ok it's not really usefull, but that's a good start. In
Prettig personeel (www.prettigpersoneel.nl - the website for which
this product has been developed), there is many pages based on the
same principle (two modes: default and back) such as changing the
password, setting the user's theme, managing contact information etc.

But now we want to do something a bit harder: create a page to manage
multiple objects.

Creating a multi-object managing page
-------------------------------------

If ou had a look at the 'collective_multimodeview_notes_samples' page,
you see that its main goal it to manage a list of notes attached to
the portal of the site.
We will create a control panel page to manage those notes. To do so,
creates notes.py and notes.pt in the control_panel package.

The notes.py will look like this::

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
	  self.request.form['obj_id'] = len(self.notes_view.get_notes()) - 1

      def _process_edit_form(self):
          self.notes_view.edit_note(
              self._get_note_id(),
              self.request.form.get('title'))

      def _process_delete_form(self):
          self.notes_view.delete_note(self._get_note_id())
          self.request.form['obj_id'] = None

So let's see what is different from the previous page (obviously a
lot):

 - modes: there is no more 'back' mode, so when submitting the form,
   we will still see the same page. Some extra modes appears to manage
   the notes.

 - default_mode: it is set to 'edit'. It means that the page will try,
   by default, to edit the first object found.

 - multi_objects: is is set to True. That means that this page can be
   used to manage multiple object. A sidebar will be shown to display
   the list of objects.

 - list_objects: when setting 'multi_objects' to True, you have to
   define this method. It returns a list of dictionnary having two
   keys: one define the id of the object and the second one the title
   displayed. 

The _check_xxx_form amd _process_xxx_form are quite similar to what we
saw previously. One point to look at is the fact that we modify the
'obj_id' entry of the request in both ``_process_add_form`` and
``_process_delete_form``. In the first case, we do that so the note
that has just been added with be considered as the current one. In the
second case, we delete the entry so the system will not consider the
deleted note as the current one (as it does not exist anymore) and
will pick the first available one.

Now let's create a template for our page::

  <tal:block tal:define="notes view/notes_view/get_notes;
                         note_exists python: bool([n for n in notes if n])">
    <form method="post"
          tal:condition="python: note_exists or view.is_add_mode"
          tal:define="note_title view/get_note_title"
          tal:attributes="action view/get_form_action">

      <tal:block tal:condition="python: view.is_add_mode or view.is_edit_mode">     
        <div tal:attributes="class python: view.class_for_field('title')">
          <label for="title">Title</label>
          <div class="error_msg"
               tal:condition="view/errors/title|nothing"
               tal:content="view/errors/title" />
          <input type="text"
                 name="title"
                 tal:attributes="value note_title" />
        </div>
      </tal:block>

      <tal:block tal:condition="view/is_delete_mode">
        <p>Are you sure you want to delete this note ?</p>

        <p class="discreet"
           tal:content="note_title" />
      </tal:block>

      <input type="hidden"
             name="obj_id"
             tal:define="obj_id view/current_object_id"
             tal:condition="obj_id"
             tal:attributes="value obj_id" />

      <span tal:replace="structure view/make_form_extras" />
    </form>

    <p tal:condition="not: python: note_exists or view.is_add_mode">
      There is no note to manage, click the '+' button to create a new one.
    </p>
  </tal:block>

In this template, we can see three important things:

 - the use of view/is_xxx_mode: this is a helper provided by
   collective.multimodeview to now what o display depending on what
   you are doing.

 - there is an hidden field called 'obj_id'. This is important, as it
   is used to know which object you are currently editing.

 - there is a default message displayed when there is no notes. Do not
   forget it. If your page rendered an empty string, the system will
   show the home page of the menu instead.

Now let's register our page. First in the __init__.py file::

    >>> from collective.mcp.samples.notes import Notes
    >>> register_page(Notes)

    >>> pages
    [<class 'collective.mcp.samples.home_message.HomeMessage'>,
     <class 'collective.mcp.samples.notes.Notes'>]

and in the configure.zcml::

  <browser:page
      for="*"
      name="collective_mcp_notes"
      class=".Notes"
      permission="zope.Public"
      template="notes.pt"
      />

Restart your server and reload the control panel, you now have two
pages available.

    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> self.browser.getLink('Notes').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=edit&widget_id=collective_mcp_notes'

As you have not played with the notes yet, the list on the right
is empty and you get a message telling you to add some notes::

    >>> import re
    >>> re.search('(<ul class="objects">\s*</ul>)', self.browser.contents).groups()
    ('<ul class="objects">...</ul>',)

    >>> "There is no note to manage, click the '+' button to create a new one." in self.browser.contents
    True

``collective.mcp`` automatically added a '+' and a '-' button that
will trigger the ``add`` and `delete` moes of your new page.
We'll click on the ``add`` button that will display the form to create
a note::

    >>> self.browser.getLink('+').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=add&widget_id=collective_mcp_notes'

    >>> '<label for="title">Title</label>' in self.browser.contents
    True

You can also notice that, when adding a new object, a new line appears
in the objects list and is shown as selected::

    >>> re.search('(<li\s*class="current">\s*<a>...</a>\s*</li>)', self.browser.contents).groups()
    ('<li class="current">...<a>...</a>...</li>',)

Now we'll add a note objects::

    >>> self.browser.getControl(name='title').value = 'A new note'
    >>> self.browser.getControl(name='form_submitted').click()

This time we are not redirected to the control panel home page but to
the ``edit`` page of the object we just added and we get a success
message::

    >>> '<dd>The note has been added</dd>' in self.browser.contents
    True

    >>> re.search('(<li class="current">\s*<a href=".*">A new note</a>\s*</li>)', self.browser.contents).groups()
    ('<li class="current">...<a href="...">A new note</a>...</li>',)

    >>> re.search('(<input type="text" name="title"\s*value="A new note" />)', self.browser.contents).groups()
    ('<input type="text" name="title" value="A new note" />',)

We now add a second note::

    >>> self.browser.getLink('+').click()
    >>> self.browser.getControl(name='title').value = 'My second note'
    >>> self.browser.getControl(name='form_submitted').click()

When saving this note is selected by default::

    >>> re.search('(<li class="current">\s*<a href=".*">My second note</a>\s*</li>)', self.browser.contents).groups()
    ('<li class="current">...<a href="...">My second note</a>...</li>',)
    
    >>> re.search('(<input type="text" name="title"\s*value="My second note" />)', self.browser.contents).groups()
    ('<input type="text" name="title"...value="My second note" />',)


More documentation
------------------

You will find more documentation in ``collective/mcp/doc``. There is
four extra documentations there::

 - modes.rst - some extra explanation about the ``modes`` attributes
   of the class.

 - restriction.rst - explains the diferent methods to restrict access
   to the pages.

 - multiobjects.rst - going a bit deeper with the multi-objects views.

 - defect.rst - some examples of what you should not do.

