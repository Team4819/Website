__author__ = 'christian'
from page_base import PageBase


class PagehubBase(PageBase):

    def __init__(self):
        self.spokes = dict()
        self.defaultPage = PageBase

    def get_page(self, request, resource):
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
            result = spoke.get_page(request, remainder)
        else:
            result = self.defaultPage(f=segment).get_page(request, remainder)

        return result


