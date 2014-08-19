from django.template import Context,loader
from pages import page

class aboutPage(page.pageBase):

    group = "public"

    def getPage(request, resource, user):
            temp = loader.get_template("home.html")
            cont = Context({})
            result = temp.render(cont)
            return result