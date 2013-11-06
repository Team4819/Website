from django.template import Context,loader
from google.appengine.ext import blobstore
from .. import auth
import AccessDenied, PageNotFound
import logging, urllib


def getPage(request, resource, user):
    if(user == 0):
        return AccessDenied.getPage(request, resource, user);
    temp = loader.get_template("PageNotFound.html")
    cont = Context({})
    result = temp.render(cont)
    return result