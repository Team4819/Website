from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2
import logging
import posts
import auth

def mailToSubscribed(post):
    sub = auth.getSubscribed()
    subscribedEmails = sub.fetch(sub.count())
    
    
    if(post.restricted == False):
        psub = auth.getPublicSubscribed()
        subscribedEmails += psub.fetch(psub.count())
    if(post.comments == 0):
        for address in subscribedEmails:
            logging.info("mailing " + address.email + " with subject as "+ post.title + " and body as " + post.content)
            mail.send_mail(sender = "mailingList@firstteam4819.appspotmail.com", to = address.email, subject = "team4819.com New post: " + post.title, body = "<p>New post by " + post.author + "</p>" + post.content, html = "<p>New post by " + post.author + "</p>" + post.content)
    else:
        lastComment = posts.getComments(post)[0]
        for address in subscribedEmails:
            mail.send_mail(sender = "mailingList@firstteam4819.appspotmail.com", to = address.email, subject = "team4819.com New comment by "+lastComment.author + " on " + post.title , body = "<p> New comment by " + lastComment.author + ": </p>" + lastComment.content, html = "<p> New comment by " + lastComment.author + ": </p>" + lastComment.content)
            
            
class mailReceptionHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Email from "+ mail_message.sender)
app = webapp2.WSGIApplication([mailReceptionHandler.mapping()], debug = True)