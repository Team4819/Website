from pagehub_base import PagehubBase
from page_base import PageBase
#from media_page import MediaPage
from UpdatesPage import UpdatesPage
__author__ = 'christian'


class pagehub(PagehubBase):
    def __init__(self):
        PagehubBase.__init__(self)
        self.spokes["none"] = PageBase(f="home")
        self.spokes["updates"] = UpdatesPage()
        #self.spokes["media"] = MediaPage()
        self.spokes["calendar"] = PageBase(group="team", permissions="r-r---")