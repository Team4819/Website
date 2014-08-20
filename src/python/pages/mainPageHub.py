from PageHubBase import PageHubBase
from PageBase import PageBase
from MediaPage import MediaPage
from UpdatesPage import UpdatesPage

class pageHub(PageHubBase):
    def __init__(self):
        self.spokes["none"] = PageBase(file="home")
        self.spokes["updates"] = UpdatesPage()
        self.spokes["media"] = MediaPage()
        self.spokes["calendar"] = PageBase(group="team")
        super(self).__init__()


__author__ = 'christian'
