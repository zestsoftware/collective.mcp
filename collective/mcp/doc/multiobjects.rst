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

Switching from one mode to the other after processing the form
--------------------------------------------------------------

We already saw in the first sample that if a 'back' mode is defined,
the system will automatically switch back to it when the form is
submitted and display the home page again.

You can also specify it for each mode. There is two solutions to do
this. The first one is in the '_process_xxx_form'. You can return the
mode to which the system will switch after processing.
For example, when you add a note, you want the user to see directly
the 'display' mode so they can asign display zones just after adding a
note. To do so, change the '_process_add_form' like this::

      def _process_add_form(self):
          # do the processing
	  return 'display'

Now when you add a note, you see the form to manage where it is
displayed.

The second solution is to update the 'modes' attribute, so you can
specify which mode is displayed after a success or after cancelling::


      modes = {'add': {'success_msg': 'The note has been added',
                       'error_msg': 'Impossible to add a note: please correct the form',
                       'submit_label': 'Add note',
		       'success_mode': 'display',
		       'cancel_mode': 'edit'}
	       ...
               }

Here it is not needed to specify cancel_mode as it is the default
one.

The main advantage of the first solution is that you can define
different modes to switch to after procesing the form, depending on
the data sent. But if you always switch to the same mode after
processing data, it might be better to declare everything in the
'modes' attribute so you have a clear overview of the relation between
modes.

