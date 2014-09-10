import webapp2
import getPage
import auth
import users

from pages import main_pagehub

from django.template import Context, loader


class MainHandler(webapp2.RequestHandler):
    def get(self, resource):
        resource = str(resource)
        users.get_session(self.request)

        temp = loader.get_template("index.html")
        hub = main_pagehub.pagehub()
        content = hub.get_page(self, resource)
        cont = Context({"content": content, "user": users.currentUser})
        result = temp.render(cont)
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(result)

app = webapp2.WSGIApplication([('/(.+)?', MainHandler)], debug=True)
