from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2
import logging
import posts
import users
import groups


def mailToSubscribed(post):
    sub = users.getSubscribed()
    subscribedEmails = sub.fetch(sub.count())
    
    
    if(post.restricted == False):
        psub = auth.getPublicSubscribed()
        subscribedEmails += psub.fetch(psub.count())
    if(post.comments == 0):
        for address in subscribedEmails:
            logging.info("mailing " + address.email)
            logging.info(" with subject as " + post.title)
            logging.info(" and body as " + post.content)
            mail.send_mail(sender = "mailingList@firstteam4819.appspotmail.com", to = address.email, subject = "team4819.com New post: " + post.title, body = "<p>New post by " + post.author + "</p>" + post.content, html = "<p>New post by " + post.author + "</p>" + post.content + "<p>----<br/>If you no longer want to receive Flat Mountain Mechanics Team Updates, you can unsubscribe by clicking <a href=\"team4819.com/python/unsubscribe?email=" + address.email + "\"/>here</a>.</p>")
    else:
        lastComment = posts.getComments(post)[0]
        for address in subscribedEmails:
            mail.send_mail(sender = "mailingList@firstteam4819.appspotmail.com", to = address.email, subject = "team4819.com New comment by "+lastComment.author + " on " + post.title , body = "<p>New comment by " + lastComment.author + ": </p>" + lastComment.content, html = "<p> New comment by " + lastComment.author + ": </p>" + lastComment.content + "<p>----<br/>If you no longer want to receive Flat Mountain Mechanics Team Updates, you can unsubscribe by clicking <a href=\"team4819.com/python/unsubscribe?email=" + address.email + "\"/>here</a>.</p>")
            
            
class mailReceptionHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Email from "+ mail_message.sender)
        messageRecieved = mail.InboundEmailMessage(self.request.body);

        if(messageRecieved.to.lower() == "teambroadcast@firstteam4819.appspotmail.com"):
            sources = auth.lookupEmail(messageRecieved.sender);
            senderName = messageRecieved.sender;
            if(sources.count() != 0): 
                source = sources[0];
                senderName = source.firstName + " " + source.lastName
                
            html = ""
            for htmlpart in messageRecieved.bodies(content_type='text/html'):
                html = html + htmlpart[1].decode()
                
            attachments = None
            if(hasattr(messageRecieved, "attachments")):
                attachments = messageRecieved.attachments

            mailToUserGroup("public",senderName,"Message from " + senderName + ": " + messageRecieved.subject,messageRecieved.body, html, attachments)

def mailToUserGroup(group, sender, subject, body, html, attachments = None):
    logging.info("Sending email broadcast to user group " + str(UserGroup))
    emails = auth.getGroupEmails(UserGroup)

    for email in emails:
        #logging.info("mailing " + email.email + " with subject as "+ messageRecieved.subject + " and body as " + messageRecieved.body)
        if attachments is None:
            mail.send_mail(sender, email.email, subject, body, html);
        else:
            mail.send_mail(sender, email.email, subject, body, html, attachments);

        
app = webapp2.WSGIApplication([mailReceptionHandler.mapping()], debug = True)
