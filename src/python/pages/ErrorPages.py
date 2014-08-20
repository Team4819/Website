__author__ = 'christian'
from django.template import Context,loader

def PageNotFound(request, resource):
        temp = loader.get_template("PageNotFound.html")
        cont = Context({})
        result = temp.render(cont)
        return result

def AccessDenied(request, resource, user):
        temp = loader.get_template("accessdenied.html")
        cont = Context({"user": user})
        result = temp.render(cont)
        return result