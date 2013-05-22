from django.template import Context,loader

def getPage(resource, user):
        temp = loader.get_template("accessDenied.html")
        cont = Context({"user": user})
        result = temp.render(cont)
        return result