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

from notes import Notes, NotesDisplay, NotesDisplayModeSwitch
register_page(Notes)
register_page(NotesDisplay)
register_page(NotesDisplayModeSwitch)

from restricted import HomeMessageRestricted, \
     HomeMessageRestrictedII, \
     HomeMessageRestrictedIII,\
     NotesRestricted
register_page(HomeMessageRestricted)
register_page(HomeMessageRestrictedII)
register_page(HomeMessageRestrictedIII)
register_page(NotesRestricted)

from defect import WrongCatIdHomeMessage, \
     ClashingWidgetIdHomeMessage,\
     NoWidgetIdPage
register_page(WrongCatIdHomeMessage)
register_page(ClashingWidgetIdHomeMessage)
register_page(NoWidgetIdPage)
