__author__ = 'christian'
from .. import users
from django.template import Context,loader

def PageNotFound(request, resource):
        temp = loader.get_template("PageNotFound.html")
        cont = Context({})
        result = temp.render(cont)
        return result

def AccessDenied(request, resource):
        temp = loader.get_template("accessdenied.html")
        cont = Context({"user": users.currentUser})
        result = temp.render(cont)
        return result