__author__ = 'christian'

import webapp2
import urllib
from .. import users
from django import template
from django.template import loader, Context


class PageBase:
    group = "public"
    f = None

    def __init__(self, group="public", f=None):
        self.group = group
        self.f = f

    def get_page(self, request, resource):
        #First, check permissions
        if users.currentUser.isGroup(self.group) or users.currentUser.isGroup("admin"):
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
                temp = loader.get_template("PageNotFound.html")
        else:
            #Red Card! We have an intruder on our site!
            temp = loader.get_template("accessdenied.html")
        cont = Context({"user": users.currentUser})
        return temp.render(cont)
