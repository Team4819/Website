import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

class Post(db.Model):
    author = db.StringProperty()
    title = db.StringProperty(multiline=True)
    shortContent = db.StringProperty(multiline=True)
    content = db.TextProperty()
    date = db.StringProperty();
    pic = db.StringProperty();
    
def archive_key(archive_name=None):
    return db.Key.from_path('Archive', "Posts" or 'default_archive')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        archive_name="Posts"
        
        posts = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY date DESC LIMIT 10",
                        archive_key("Posts"))
        for post in posts:
            self.response.out.write('<div class="post">')
            self.response.out.write('<h3>%s</h3>' % post.title)
            self.response.out.write('<div class="text">%s</div>' % post.shortContent)
            if post.author:
                self.response.out.write('<div class="Author"><b>By %s</b></div>' % post.author)
            else:
                self.response.out.write('<p class="Author"><b>By Anonomous</b></p>')
            self.response.out.write('<p class="Date">%s</p>' % post.date)
            self.response.out.write('</div>\n')
            
        self.response.out.write("""
          <form action="/addPost?%s" method="post">
            <div><p>Title</p><textarea name="title" rows="3" cols="60"></textarea></div>
            <div><p>pic</p><textarea name="pic" rows="3" cols="60"></textarea></div>
            <div><p>content</p><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><p>shortContent</p><textarea name="shortContent" rows="3" cols="60"></textarea></div>
            <div><p>Author</p><textarea name="author" rows="3" cols="60"></textarea></div>
            <div><p>Date</p><textarea name="date" rows="3" cols="60">%s</textarea></div>
            <div><input type="submit" value="Submit Post"></div>
          </form>
        </body>
      </html>""" % (urllib.urlencode({'archive_name': archive_name}),datetime.date.isoformat(datetime.date.today())))
                
        

class addPost(webapp2.RequestHandler):
    def post(self):
        archive_name = "Posts"
        post = Post(parent=archive_key(archive_name))
        
        if users.get_current_user():
            post.author = users.get_current_user().nickname()
        
        post.content = self.request.get('content');
        post.title = self.request.get('title');
        post.shortContent = self.request.get('shortContent');
        post.pic = self.request.get('pic');
        post.date = self.request.get('date');
        post.author = self.request.get('author');
        post.put()
        self.redirect('/MainPage?' + urllib.urlencode({'archive_name' : archive_name}))
    


app = webapp2.WSGIApplication([('/MainPage', MainPage), ('/addPost', addPost)], debug=True)    

