__author__ = 'christian'
from django.template import loader, Context
from page_base import PageBase
from .. import users
import ErrorPages


class PagehubBase(PageBase):

    def __init__(self, user="nobody", group="group", permissions="r-r-r-"):
        PageBase.__init__(self, user=user, group=group, permissions=permissions)
        self.spokes = dict()
        self.defaultPage = PageBase

    def get_page(self, request, resource, parent=None):
        r, w = self.check_permissions()
        if r:
            segment = resource.split("/")[0]
            split = resource[1:].split("/", 1)
            if len(split) > 1:
                remainder = split[1]
            else:
                remainder = ""

            if segment is None or segment == "":
                segment = "none"
            segment = segment.lower()
            if segment in self.spokes:
                spoke = self.spokes[segment]
                result = spoke.get_page(request, remainder, self)
            else:
                result = self.defaultPage(f=segment).get_page(request, remainder, self)
        else:
            return ErrorPages.AccessDenied(request, resource)
        return result


