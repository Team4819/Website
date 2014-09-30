__author__ = 'christian'

import webapp2
import urllib
import ErrorPages
from .. import users
from django import template
from django.template import loader, Context


class PageBase:
    group = "public"
    user = "public user"
    permissions = "r-r-r-"

    f = None

    def __init__(self, f=None, user="nobody", group="group", permissions="r-r-r-"):
        self.user = user
        self.group = group
        self.permissions = permissions
        self.f = f

    def check_permissions(self):
        r = self.permissions[4] is "r"
        w = self.permissions[5] is "w"
        if users.currentUser.lcaseName is self.user:
            r = r or self.permissions[0] is "r"
            w = w or self.permissions[1] is "w"
        if users.currentUser.isGroup(self.group):
            r = r or self.permissions[2] is "r"
            w = w or self.permissions[3] is "w"
        if users.currentUser.isGroup("admin"):
            r = True
            w = True
        return r, w

    def get_page(self, request, resource):
        #First, check permissions
        r, w = self.check_permissions()
        if r:
            #Check and see if we must ignore the request and fetch our own file
            if self.f is None:
                #apparently not
                pagefile = str(urllib.unquote(resource)).lower()
            else:
                #Ok, will get own file
                pagefile = self.f
            try:
                temp = loader.get_template(pagefile + ".html")
            except template.TemplateDoesNotExist:
                #Oops, never heard of that file!
                return ErrorPages.PageNotFound(request, resource)
        else:
            #Red Card! We have an intruder on our site!
            return ErrorPages.AccessDenied(request, resource)
        cont = Context({"user": users.currentUser})
        return temp.render(cont)
