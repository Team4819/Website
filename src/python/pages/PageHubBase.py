from PageBase import PageBase
import webapp2
import urllib

class PageHubBase(PageBase):
    spokes = dict()
    defaultPage = PageBase()

    def getPage(self, request, resource, user):
        segment = resource.split("/")[0]
        remainder = resource[1:].split("/", 1)[-1]

        if(segment != None):
            segment = segment.lower()
        try:
            spoke = self.spokes[segment]
            result = spoke.getPage(request, remainder, user)

        except KeyError:
            result = self.defaultPage.getPage(request, remainder, user)

        return result







__author__ = 'christian'
