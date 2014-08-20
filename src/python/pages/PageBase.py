__author__ = 'christian'

import webapp2
import urllib
from django import template
from django.template import loader, Context
from pages import PageNotFound

class PageBase:
    group = "public"
    file = None
    def __init__(self, group="public", file=None ):
        self.group = group
        self.file = file



    def getPage(self, request, resource, user):
        #First, check permissions
        if user.isGroup(self.group) or user.isGroup("admin"):
            #Check and see if we must ignore the request and fetch our own file
            if self.file is None:
                #apparently not
                pageFile = str(urllib.unquote(resource)).lower()
            else:
                #Ok, will get own file
                pageFile = file
            try:
                temp = loader.get_template(pageFile + ".html")
            except template.TemplateDoesNotExist:
                #Oops, never heard of that file!
                temp = loader.get_template("PageNotFound.html")
        else:
            #Red Card! We have an intruder on our site!
            temp = loader.get_template("AccessDenied.py")
        cont = Context({"user": user})
        return temp.render(cont)
