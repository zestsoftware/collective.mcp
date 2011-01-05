class Category(object):
    def __init__(self, cat_id, title, before = None, after = None):
        self.id = cat_id
        self.title = title

        self.before = before
        self.after = after

    def __repr__(self):
        return 'Category: %s' % self.id

    def getTitle(self):
        return self.title
