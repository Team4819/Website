from django.template import Context,loader
from google.appengine.ext import blobstore
from .. import auth
import AccessDenied, PageNotFound
import logging, urllib
from src.python.pages.ErrorPages import AccessDenied


def getPage(request, resource, user):
    if(user == 0):
        return AccessDenied(request, resource, user);
    temp = loader.get_template("profile.html")
    cont = Context({})
    result = temp.render(cont)
    return result