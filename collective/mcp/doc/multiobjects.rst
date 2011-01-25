Managing multiple objects in a page
===================================

The README file shown how to create a simple page to manage multiple
objects. In this file you'll find some example to go a bit further.


Adding extra buttons to multi-objects views
-------------------------------------------

You might need more buttons in the list than '+' and '-' ones. Let's
say for example that you want the notes to be displayed only on
certain areas of the site. This setting is different for each note.

To do so, we will first declare a new mode in the list and the methods
needed to proces it::
  
  class Notes(ControlPanelPage):
      ...
      modes = {...,
               'display': {'success_msg': 'The display zones for the ' +\
                           'note has been updated',
                       	   'submit_label': 'Change display zones'}
               }

      ...

      def _check_display_form(self):
          # do some checks.
	  return True

      def _process_display_form(self):
          # process the form

Now we also declare an extra button displayed in the list, after the
'-' one::

      multi_objects_extra_buttons = [
          {'mode': 'display',
           'title': 'Change display zones',
           'icon': 'display_button.gif'}]

The 'multi_object_extra_buttons' property is a list of
dictionnary. For each you define:

 - which is the mode used when clicking the button

 - the text displayed as a title for the button

 - the icon used (if you use the default theme, the best size is 15px
   x 15px)

Now let's check that our new button is displayed (and works) and add a
new note to manage where it is displayed::

    >>> from collective.mcp import register_page
    >>> from collective.mcp.samples import NotesDisplay
    >>> register_page(NotesDisplay)

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> self.browser.getLink('Displayed notes').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=edit&widget_id=collective_mcp_notes_display'
    >>> 'display_button.png' in self.browser.contents
    True
    >>> "There is no note to manage, click the '+' button to create a new one." in self.browser.contents
    True
    >>> self.browser.getLink('+').click()
    >>> self.browser.getControl(name='title').value = 'A new note'
    >>> self.browser.getControl(name='form_submitted').click()

Now if we click on the button, we will see the form to edit the
display zones for our object::

    >>> self.browser.getLink('Change display zones').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=display&widget_id=collective_mcp_notes_display'

    >>> 'Set where the note should be displayed' in self.browser.contents
    True

Let's select some and save it::

    >>> self.browser.getControl('home').selected = True
    >>> self.browser.getControl('news').selected = True
    >>> self.browser.getControl(name='form_submitted').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel'
    >>> '<label for="title">Title</label>' in self.browser.contents
    True

Ok we have returned to the 'edit' view for this note. Clicking on the
display button again should show our form with the values saved::

    >>> self.browser.getLink('Change display zones').click()
    >>> self.browser.getControl('home').selected
    True
    >>> self.browser.getControl('news').selected
    True

There is not (yet) much more things to explain for multi-object
views.
