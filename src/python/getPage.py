import webapp2
import users
from pages import main_pagehub


class GetPageHandler(webapp2.RequestHandler):
        def get(self, resource):
            users.get_session(self.request)
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(main_pagehub.pagehub().get_page(self, resource))
            

app = webapp2.WSGIApplication([('/Pages/(.+)?', GetPageHandler)], debug=True)
