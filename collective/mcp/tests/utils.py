from HTMLParser import HTMLParser

class McpHtmlParser(HTMLParser):
    """ The goal of this parser is to
    extract the usefull part of the browser contents:
     - the list of control panel categories available
     - the list of pages displayed
     - the list of buttons available for multi-objects pages
    """

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)

        # True when a div with id 'subpage' is found in
        # the container.
        self.subpage_rendered = False

        # List of buttons rendered,
        # Each button is registered as a dictionnary:
        # {'href': ..., 'img': ...}
        self.multi_object_buttons = []

        # ist of objects in the list,
        # Each is registered as a dictionnary:
        # {'href':..., 'text': ..., 'current': True/False}
        self.multi_objects = []

        # List if items on the home page.
        # [{'title': 'Settings',
        #   'pages': [{'href': ..., 'title': ..., 'icon': ...},
        #             {'href': ..., 'title': ..., 'icon': ...},
        #             ...]},
        #  {...}]
        self.home_page = []

        # List of nodes encountered
        self.path = []

        # A few flags: they should all be reseted to False at the end.
        self.in_control_panel = False
        self.in_control_panel_header = False
        self.in_control_panel_content = False
        self.in_objects_list = False
        self.in_objects = False
        self.in_buttons = False
        self.in_menu = False

    def print_home_page(self):
        print 'Home page'
        for item in self.home_page:
            print ' - %s:' % item.get('title', 'No title')

            for p in item.get('pages', []):
                print '   + %s (%s, %s)' % (
                    p.get('title', 'no title'),
                    p.get('icon', 'no icon'),
                    p.get('href', 'no href'))

    def print_objects(self):
        print 'Objects'
        for o in self.multi_objects:
            print '%s %s (%s)' % (
                o.get('current', False) and '-->' or '   ',
                o.get('text', 'No text'),
                o.get('href', 'No href'))

    def print_buttons(self):
        print 'Buttons'
        for b in self.multi_object_buttons:
            print ' - %s (%s)' % (
                b.get('img', 'no image'),
                b.get('href', 'no href'))                      

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        tag_id = attrs.get('id', '')
        tag_classes = attrs.get('class', '')
        self.path.append({'tag': tag,
                          'id': tag_id,
                          'class': tag_classes})
        
        if tag == 'div':
            if tag_id == 'control_panel_container':
                self.in_control_panel = True
            elif tag_id == 'control_panel_header':
                self.in_control_panel_header = True
            elif tag_id == 'control_panel_content':
                self.in_control_panel_content = True
            elif tag_id == 'subpage':
                self.subpage_rendered = True
            elif tag_id == 'objects_list':
                self.in_objects_list = True

        if tag == 'ul':
            if 'objects' in tag_classes and self.in_objects_list:
                self.in_objects = True
            if 'buttons' in tag_classes and self.in_objects_list:
                self.in_buttons = True
            if tag_classes == 'menu' and self.in_control_panel_content:
                self.in_menu = True

        if tag == 'li':
            if self.in_objects:
                current = 'current' in tag_classes
                self.multi_objects.append({'current': current})
                
        if tag == 'a':
            if self.in_objects and self.multi_objects:
                self.multi_objects[-1]['href'] = attrs.get('href', '')
            elif self.in_buttons:
                self.multi_object_buttons.append(
                    {'href': attrs.get('href', '')})                
            elif self.in_menu and self.home_page:
                self.home_page[-1]['pages'].append({'href': attrs.get('href', '')})

    def handle_endtag(self, tag):
        if not self.path:
            return

        t = self.path.pop()
        tag_id = t.get('id', '')
        tag_classes = t.get('class', '')

        if t['tag'] == 'div':
            if tag_id == 'control_panel_container':
                self.in_control_panel = False
            elif tag_id == 'control_panel_header':
                self.in_control_panel_header = False
            elif tag_id == 'control_panel_content':
                self.in_control_panel_content = False
            elif tag_id == 'subpage':
                self.subpage_rendered = False
            elif tag_id == 'objects_list':
                self.in_objects_list = False

        if t['tag'] == 'ul':
            if 'objects' in tag_classes and self.in_objects_list:
                self.in_objects = False
            if 'buttons' in tag_classes and self.in_objects_list:
                self.in_buttons = False
            if tag_classes == 'menu' and self.in_control_panel_content:
                self.in_menu = False
                
    def handle_startendtag(self, tag, attrs):
        attrs = dict(attrs)

        if  tag == 'img':
            if self.in_buttons and self.multi_object_buttons:
                self.multi_object_buttons[-1]['img'] = attrs.get('src', '')
            elif self.in_menu and self.home_page and self.home_page[-1]['pages']:
                self.home_page[-1]['pages'][-1]['icon'] = attrs.get('src', '')

    def handle_data(self, data):
        if not self.path:
            return
        tag = self.path[-1]

        if tag['tag'] == 'a':
            if self.in_objects and self.multi_objects:
                self.multi_objects[-1]['text'] = data
            elif self.in_buttons and self.multi_object_buttons:
                self.multi_object_buttons[-1]['text'] = data

        if tag['tag'] == 'span':
            if self.in_menu:
                if 'spacer' in tag['class']:
                    self.home_page.append({'title': data, 'pages': []})
                elif  self.home_page and self.home_page[-1]['pages']:
                    self.home_page[-1]['pages'][-1]['title'] = data
