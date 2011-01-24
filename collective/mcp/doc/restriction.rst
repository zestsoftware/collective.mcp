Restricting access to pages
===========================

This tests shows some more example on how to restrict access to
subpages on the control panel. Our examples are based on pages defined
in the samples (see file ``collective/mcp/samples/restricted.py``).

It might be usefull to have a look to the README before reading this file.

Block access with ZCML
----------------------

The first solution is pretty classic. In the ``configure.zcml`` file,
where you define the pages. you can define a custom permission instead
of ``Zope.Public``. For example, you can define the ``Home message``
control panel page this way::

  <browser:page
      for="*"
      name="collective_mcp_home_message"
      class=".HomeMessage"
      permission="cmf.ManagePortal"
      template="home_message.pt"
      />

Ok, by doing so, only managers will be able to set the ``Home
message``. That's a good thing (even if, in this case, it might be
better to use the real Plone control panel which is intended to be
used by managers).

In the samples, we defined a second view called ``HomeMessageRestricted``,
inheriting from the previous one.
We will register it to see if the blocking is effective::

    >>> from collective.mcp import register_page
    >>> from collective.mcp.samples import HomeMessageRestrictedII
    >>> register_page(HomeMessageRestrictedII)

For the moment, we are anonymous user, so we should not see our
restricted page::

    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'Home message (restricted to admin)' in self.browser.contents
    False

We login and reload the control panel::

    >>> self.login_as_manager()
    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'Home message (restricted to admin)' in self.browser.contents
    True

    >>> self.browser.getLink('Home message (restricted to admin)').click()
    >>> restricted_home_url = self.browser.url
    >>> restricted_home_url
    'http://nohost/plone/control_panel?mode=default&widget_id=collective_mcp_home_message_restricted'

If someone knows the URL, it is still impossible for him to access the
page (well, he does not get an Unauthorized message, he just sees the
normal control panel home page)::

    >>> self.browser.open('http://nohost/plone/logout')
    >>> self.browser.open(restricted_home_url)
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    False
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    True

Block access using the ``view_permission`` attribute
----------------------------------------------------

The ``view_permission`` attribute is inherited from
``collective.multimodeview``. When setting this attribute, only users
with the described permission will be allowed to see the page.

The page is defined this way::

  class HomeMessageRestrictedII(HomeMessage):
      zcml_id = 'collective_mcp_home_message_restrictedII'
      widget_id = 'collective_mcp_home_message_restrictedII'
      title = 'Home message (restricted using "permission" attribute)'

      view_permission = 'Manage portal'

If we access is as a normal user, we do not see it::

    >>> self.browser.open('http://nohost/plone/logout')
    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'Home message (restricted using "permission" attribute)' in self.browser.contents
    False

But as a manager, it is visible::

    >>> self.login_as_manager()
    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'Home message (restricted using "permission" attribute)' in self.browser.contents
    True

    >>> self.browser.getLink('Home message (restricted using "permission" attribute)').click()
    >>> restricted_home_url_2 = self.browser.url
    >>> restricted_home_url_2
    'http://nohost/plone/control_panel?mode=default&widget_id=collective_mcp_home_message_restrictedII'

And again, even if you know the URL of the page, you can not access it
if you do not have the required permission, you simply see the control
panel home page::

    >>> self.browser.open('http://nohost/plone/logout')
    >>> self.browser.open(restricted_home_url_2)
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    False
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    True

Using ``view_permission`` method or restricting the access in ZCML
gives the same kind of results, so the choice is yours.

A third method to block access to a complete page is to override the
``is_shown`` method.

Block access using the ``is_shown`` method
------------------------------------------

Like the ``view_permission`` attribute, the ``is_shown`` method is
inherited from ``collective.multimodeview``. By default, the
``is_shown`` method simply check that the permission defined by
``view_permission``, if defined, is granted to the user.

In this third example, we'll create another copy of the ``Home
message`` page, this time only accessible if your are not a manager::

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

    >>> from collective.mcp.samples import HomeMessageRestrictedIII
    >>> register_page(HomeMessageRestrictedIII)

We connect as a normal user::

    >>> self.browser.open('http://nohost/plone/logout')
    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'Home message (restricted using "is_shown" method)' in self.browser.contents
    True

    >>> self.browser.getLink('Home message (restricted using "is_shown" method)').click()
    >>> restricted_home_url_3 = self.browser.url
    >>> restricted_home_url_3
    'http://nohost/plone/control_panel?mode=default&widget_id=collective_mcp_home_message_restrictedIII'

And as a manager, we do not see it and can not access the page even
with the URL::

    >>> self.login_as_manager()
    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'Home message (restricted using "is_shown" method)' in self.browser.contents
    False
    >>> self.browser.open(restricted_home_url_3)
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    False
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    True

Using partial restriction for a page
------------------------------------

Restricting access for the ``Home message`` page was pretty simple, as
it provided only one behavior (setting the home mesage). But
sometimes, you will need to restrict access only partially.

In the ``Notes`` view, some users should be able to create and
edit note, but not delete them. You can not specify a single
permission to view the page, you need more.
Let's consider you have two permissions:

 - myproduct.managenotes: grant the access to this page and allows to
   add and edit notes.

 - myproduct.deletenotes: user's with this permission can delete a
   note.

For the moment, everyone with the first permission is able to delete
notes and you do not want it.
The first thing we have to do is to declare the 'modes' attribute as a
property. Users do not have the 'myproduct.deletenote' permission will
not have access to the delete mode::

  @property
  def modes(self):
      modes = {'add': {'success_msg': 'The note has been added',
                       'error_msg': 'Impossible to add a note: please correct the form',
                       'submit_label': 'Add note'},
               'edit': {'success_msg': 'The note has been edited',
                        'submit_label': 'Edit note'}}
      if self.checkPermission('myproduct: delete notes'):
             modes['delete'] = {'success_msg': 'The note has been deleted',
                                'submit_label': 'Delete note'}
      return modes

This way, a user that does not have the required permission will not
be able to switch to delete mode (as, for the view, this mode does not
exist). Any attempt to use the delete mode will switch back to the
default one.

But the '-' button is sill shown. To solve this, we will override the
'multi_objects_buttons' attributes::

  @property
  def multi_objects_buttons(self):
      buttons = ['add']
      if self.checkPermission('myproduct: delete notes'):
          buttons.append('delete')

      return buttons

Doing so, the '-' button is only shown when the user has the needed
permission.

In the samples we created a NotesRestricted view. It provides almost
the same behavior than explained before, except that the view is
visible to everyone, but the delete mode needs the 'Manage portal'
permission (we did not want to add custom permissions just for testing
purposes)::

    >>> from collective.mcp.samples import NotesRestricted
    >>> register_page(NotesRestricted)

As an anonymous  user, we see the page at the control panel root::

    >>> self.browser.open('http://nohost/plone/logout')
    >>> self.browser.open('http://nohost/plone/control_panel/')
    >>> 'Partially restricted notes' in self.browser.contents
    True
    >>> self.browser.getLink('Partially restricted notes').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=edit&widget_id=collective_mcp_notes_restricted'

We see the button to add a note but not the one to delete one::

    >>> 'mcp_add_button.gif' in self.browser.contents
    True
    >>> 'mcp_del_button.gif' in self.browser.contents
    False

Now doing the same as the manager, we will see the delete button::

    >>> self.login_as_manager()
    >>> self.browser.open('http://nohost/plone/control_panel/')

    >>> self.browser.getLink('Partially restricted notes').click()
    >>> 'mcp_add_button.gif' in self.browser.contents
    True
    >>> 'mcp_del_button.gif' in self.browser.contents
    True

Of course we do not have any note for the moment, so we'll add one to
access the ``delete`` mode::

    >>> "There is no note to manage, click the '+' button to create a new one." in self.browser.contents
    True
    >>> self.browser.getLink('+').click()
    >>> self.browser.getControl(name='title').value = 'A new note'
    >>> self.browser.getControl(name='form_submitted').click()

Now we can use the ``delete`` button::

    >>> self.browser.getLink('-').click()
    >>> delete_url = self.browser.url
    >>> delete_url
    'http://nohost/plone/control_panel?mode=delete&widget_id=collective_mcp_notes_restricted'
    >>> "Are you sure you want to delete this note ?" in self.browser.contents
    True

And if a non-manager user tries to delete the note (by opening the
page switching to delete mode, he will not see the form to delete the
not but the form to edit one (the default mode again)::

    >>> self.browser.open('http://nohost/plone/logout')
    >>> self.browser.open(delete_url)
    >>> "Are you sure you want to delete this note ?" in self.browser.contents
    False
    >>> '<label for="title">Title</label>' in self.browser.contents
    True
