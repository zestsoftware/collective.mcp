import logging

from Products.Five import BrowserView

from collective.mcp import categories, pages, sorted_categories, custom_sort

logger = logging.getLogger('collective.multimodeview')

class MacControlPanel(BrowserView):
    def base_url(self):
        return '%s/%s' % (self.context.absolute_url(),
                          self.__name__)
    
    def filter_pages(self):
        """ Provides a dictionnary of pages that are
        viewable by the user.

        Returns a dictionnary where the keys are the
        pages ids and values the page objects initialized.
        """
        pages_dict = {}
        for pclass in pages:
            page = self.context.restrictedTraverse(
                '@@%s' % pclass.zcml_id)
            page.view = self

            if not page.is_shown():
                continue

            try:
                page_id = page.widget_id

                if page_id in pages_dict:
                    msg = "widget_id '%s' is already used. Choose another one."
                    logger.warn(msg % page_id)
                    continue

                pages_dict[page_id] = page
            except AttributeError:
                logger.warn("You did not provide 'widget_id' for class %s" % pclass)

        return pages_dict

    def __call__(self):
        pages_dict = self.filter_pages()
        form = self.request.form
        requested_id = form.get('widget_id', None)

        if requested_id in pages_dict:
            # Ok we'll just render the page requested.
            page = pages_dict[requested_id]
            rendered = page()
            
            # The is a special mode for sub-page called back.
            # In this mode, the page is not shown but the main menu.
            if page.mode != 'back':
                self.sub_page = page
                self.sub_page_rendered = rendered
                return self.index()

        # No page (or an incorrect) page was requested, so we
        # render the default view with all the icons.
        # We build a temp dictionnary to store
        # categories and page.
        # This will then be treated for:
        # - keeping the same order than the original categories list.
        # - removing the empty categories
        categories_tmp = {}

        for page_id, page in pages_dict.items():
            page_cat = page.category
            if not page_cat in categories_tmp:
                categories_tmp[page_cat] = []

            categories_tmp[page_cat].append(page)

        # Now be build the real 'categories' attribute that will be used
        # to render the main page.
        self.categories = []

        for cat in sorted_categories():
            if not cat.id in categories_tmp:
                # Well, there's no page for this category.
                continue

            self.categories.append({'category': cat,
                                    'pages': custom_sort(
                                        categories_tmp[cat.id],
                                        'widget_id')
                                    })

        return self.index()
