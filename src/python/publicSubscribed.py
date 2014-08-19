__author__ = 'christian'
import users
import hashlib
import logging
import string
from google.appengine.ext import db
import random

class publicSubscribed(db.Model):
    email = db.EmailProperty()

def createPublicSubscribed(email):
    uemails = db.GqlQuery('SELECT * '
                          'FROM User '
                          'WHERE ANCESTOR IS :1 AND email = :2',
                          db_key(), email)
    pemails = findPublicEmail(email)
    if uemails.count() != 0 | pemails.count():
        return
    sub = publicSubscribed(parent=users.db_key())
    sub.email = email
    sub.put()

def findPublicEmail(email):
    return db.GqlQuery('SELECT * '
                       'FROM publicSubscribed '
                       'WHERE ANCESTOR IS :1 AND email = :2',
                       users.db_key(), email)

def getPublicSubscribed():
    return db.GqlQuery('SELECT email '
                       'FROM publicSubscribed '
                       'WHERE ANCESTOR IS :1 ',
                       UserTable_key())
