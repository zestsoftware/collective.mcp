import logging

from Products.Five import BrowserView

from collective.mcp import categories, pages
from collective.mcp import McpMessageFactory as _

logger = logging.getLogger('collective.multimodeview')

class MacControlPanel(BrowserView):
    def base_url(self):
        return '%s/%s' % (self.context.absolute_url(),
                          self.__name__)
    
    def filter_pages(self):
        """ Provides a list of pages that are
        viewable by the user.
        """
        filtered_pages = []
        used_ids = []

        for pclass in pages:
            try:
                page = self.context.restrictedTraverse(
                    '@@%s' % pclass.zcml_id)
            except:
                # The page does not exist in this context or is not
                # accessible for the user.
                logger.info('Page "%s" not found' % pclass.zcml_id)
                continue

            page.view = self
            try:
                page_id = page.widget_id

                if page_id in used_ids:
                    msg = "widget_id '%s' is already used. Choose another one."
                    logger.warn(msg % page_id)
                    continue

                if not page.is_shown():
                    logger.info('Page "%s" not visible' % pclass.zcml_id)
                    continue

                filtered_pages.append(page)
                used_ids.append(page_id)

            except AttributeError:
                logger.warn("You did not provide 'widget_id' for class %s" % pclass)

        return filtered_pages

    def __call__(self):
        pages = self.filter_pages()

        form = self.request.form
        requested_id = form.get('widget_id', None)

        for page in pages:            
            if requested_id == page.widget_id:
                # Ok we'll just render the page requested.
                rendered = page()

                # There is a special mode for sub-page called 'back'.
                # In this mode, the page is not shown but the main menu.
                if page.mode != 'back':
                    self.sub_page = page
                    self.sub_page_rendered = rendered
                    return self.index()

                # Well, no need to look for other pages.
                break

        # No page (or an incorrect) page was requested, so we
        # render the default view with all the icons.
        # We build a temp dictionnary to store
        # categories and page.
        # This will then be treated for:
        # - keeping the same order than the original categories list.
        # - removing the empty categories
        categories_tmp = {}

        for page in pages:
            page_cat = page.category
            if not page_cat in categories_tmp:
                categories_tmp[page_cat] = []

            categories_tmp[page_cat].append(page)

        # Now be build the real 'categories' attribute that will be used
        # to render the main page.
        self.categories = []

        for cat in categories:
            if not cat.id in categories_tmp:
                # Well, there's no page for this category.
                continue

            cat.context = self.context
            self.categories.append({'category': cat,
                                    'pages': categories_tmp[cat.id]
                                    })

        return self.index()
