Playing with the modes
======================

Has you might have seen in the README (if you read this file buried in
the package I guess you already had a look at the README file), the
pages in the control panel are inheriting from
``collective.multimodeview`` and are using modes to know what to do
depending on the form submitted. The README file explained most of the
basic things about the modes. The file will explain a bit more.


The ``back`` mode
-----------------

This mode is a special one created for ``collective.mcp``. When a view
switches to ``back`` mode, then the homepage of the control panel is
shown.

For example, the sample page ``Home message`` switches to ``back`` mode
when saving the form::

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> self.browser.getLink('Home message').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=default&widget_id=collective_mcp_home_message'
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    False
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    True

    >>> self.browser.getControl(name='msg').value = 'My new home message - welcome :)'
    >>> self.browser.getControl(name='form_submitted').click()
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    True
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    False

The ``cancel`` mode
-------------------

Contrary to the ``back`` mode, having a mode called ``cancel`` does
not do anything special.
We will talk here about the property named ``cancel_mode`` for the
pages. This property defines to which mode the user will be redirected
when he hits the cancel button.

For control panel pages, the default behaviour is to fall back to
``back`` mode if the page knows this mode or to the default mode
(specified by the ``default_mode`` property).

For example, in the ``Home message`` page, if the user hits the cancel
button, he is redirected to the control panel home page::

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> self.browser.getLink('Home message').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=default&widget_id=collective_mcp_home_message'
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    False
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    True
    >>> self.browser.getControl(name='form_cancelled').click()
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    True
    >>> '<label for="msg">Message:</label>' in self.browser.contents
    False

In the ``Notes`` pages, there is no ``back`` mode defined. So, when
hitting ``cancel``, he will see the ``edit`` mode (as it is the
default one)::

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> self.browser.getLink('Notes').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=edit&widget_id=collective_mcp_notes'
    >>> "There is no note to manage, click the '+' button to create a new one." in self.browser.contents
    True
    >>> self.browser.getLink('+').click()
    >>> self.browser.getControl(name='title').value = 'A new note'
    >>> self.browser.getControl(name='form_submitted').click()
    >>> self.browser.getLink('-').click()
    >>> self.browser.getControl(name='form_cancelled').click()
    >>> '<img src="++resource++collective_mcp_home.png"' in self.browser.contents
    False
    >>> '<label for="title">Title</label>' in self.browser.contents
    True

If needed, you can also manually set the ``cancel_mode`` attribute on
your page (for example, you define a ``back`` mode but you do not want
to switch to hit when hitting the cancel button.

Success/cancel mode depending on the current mode
-------------------------------------------------

If you defined multiple modes, you might want the system to react
differently after successfully processing the form or cancelling
depending on the current mode.

To do so, the attributes ``cancel_mode`` and ``default_mode`` are not
enough (well, they are if you define them as properties and did some
magic, but there's a better way to do it).

The first solution works only when the form has been succesfully
processed. As we can see in the source code of the ``Home message`` page,
the _process_default_form returns 'back'::

    def _process_default_form(self):
        self.notes_view.set_home_message(
            self.request.form.get('msg', ''))
        return 'back'

That tells the system that, after having succesfully processed the
form, the viez should switch to ``back`` mode (and so display the
control panel home).

This can be used in every ``_process_xxx_form`` method, as long as the
string returned is a mode known to the view (if we had returned
'blabla', which is not a mode of the view, then the system would have
switched to the default mode, named ``default`` in this case).

The main limitation of this system is that, when the user hits the
cancel button, we can not specify which mode to use.

The second solution is to declare two extra keys in the dictionnaries
defining the modes.
For example, the modes attribute for the ``Notes`` page could be
defined this way::

    modes = {'add': {'success_msg': 'The note has been added',
                     'error_msg': 'Impossible to add a note: please correct the form',
                     'submit_label': 'Add note',
                     'cancel_mode': 'add',
 		     'success_mode': 'display'},
	     ...}

This way, once the user sumbits the the form to add a new note, he is
redirected to the page to set where this note will be displayed::

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> self.browser.getLink('Mode switching notes').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=edit&widget_id=collective_mcp_notes_mode_switch'
    >>> self.browser.getLink('+').click()
    >>> self.browser.getControl(name='title').value = 'A new note'
    >>> self.browser.getControl(name='form_submitted').click()
    >>> "<p>Set where the note should be displayed</p>" in self.browser.contents
    True

And when he cancels the form to add one, he is redirected to the form
to add one (instead of the form to edit one)::

    >>> self.browser.open('http://nohost/plone/control_panel')
    >>> self.browser.getLink('Mode switching notes').click()
    >>> self.browser.url
    'http://nohost/plone/control_panel?mode=edit&widget_id=collective_mcp_notes_mode_switch'
    >>> self.browser.getLink('+').click()
    >>> self.browser.getControl(name='form_cancelled').click()
    >>> self.browser.getControl(name='title')
    <Control name='title' type='text'>
    >>> '<a>...</a>' in self.browser.contents
    True

Note: if _process_xxx_form returns a mode, that will override the
``sucess_mode`` defined for the mode. This might be useful when you
want in some cases (extra permission for the user or specific data
entered) to override the default ``success_mode``.
