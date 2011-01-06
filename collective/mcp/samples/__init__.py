from collective.mcp import Category, register_category, register_page

register_category(
    Category('personal',
             u'Personal preferences')
    )

register_category(
    Category('settings',
             'Settings',
             after='personal')
    )

from home_message import HomeMessage
register_page(HomeMessage)
