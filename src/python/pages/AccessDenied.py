from django.template import Context,loader

def getPage(request, resource, user):
        temp = loader.get_template("accessdenied.html")
        cont = Context({"user": user})
        result = temp.render(cont)
        return result
