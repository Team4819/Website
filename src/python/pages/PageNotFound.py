from django.template import Context,loader

def getPage(request, resource):
        temp = loader.get_template("PageNotFound.html")
        cont = Context({})
        result = temp.render(cont)
        return result