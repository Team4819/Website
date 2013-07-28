import hashlib
import os
import logging
import string
from google.appengine.ext import db
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class User(db.Model):
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    lcaseName = db.StringProperty()
    passwordHash = db.StringProperty()
    permissions = db.IntegerProperty()
    keyHash = db.StringProperty()
    email = db.EmailProperty()
    subscribed = db.BooleanProperty()
    number = db.PhoneNumberProperty()
    
class publicSubscribed(db.Model):
    email = db.EmailProperty()
    
class publicUser(User):
    firstName = "Public"
    lastName = "User"
    subscribed = False
    permissions = 0
    
class authKey(db.Model):
    userKey = db.StringProperty()
    authKey = db.StringProperty()
    expirationDate = db.DateTimeProperty()
    
def UserTable_key():
    return db.Key.from_path('UserTable-version', 'UserTable-1')

def KeyTable_key():
    return db.Key.from_path('KeyTable-version', 'KeyTable-1')

class invalidLogon(Exception):
    pass

def authorize(key):
    keyhash = hashlib.md5(key).hexdigest()
    try:
        user = db.GqlQuery("SELECT * "
                           "FROM User "
                           "WHERE ANCESTOR IS :1 AND keyHash = :2 "
                           "Limit 1 ",
                           UserTable_key(), keyhash)[0]
    except IndexError:
        user = publicUser
    if(user.subscribed == None):
        user.subscribed = False;
        user.put();
    return user
    
def logIn(firstName, lastName, password):
    try:
        user = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE ANCESTOR IS :1 AND lcaseName = :2 "
                        "Limit 1 ",
                        UserTable_key(), str(firstName).lower() + " " + str(lastName).lower())[0]
    except IndexError:
        user = publicUser
        raise(invalidLogon)
        
        
    if (user.passwordHash != hashlib.md5(password).hexdigest()): raise(invalidLogon)
    
    key = id_generator(16)
    h = hashlib.md5(key).hexdigest()
    user.keyHash = h
    user.put()
    return key

def createUser(firstName, lastName, email, number, password):
    newuser = User(parent=UserTable_key())
    newuser.firstName = firstName
    newuser.lastName = lastName
    newuser.lcaseName = str(firstName).lower() + " " + str(lastName).lower()
    newuser.passwordHash = hashlib.md5(password).hexdigest()
    newuser.permissions = 1
    newuser.email = email
    pemail = findPublicEmail(email)
    if(pemail.count() != 0):
        pemail[0].delete();
        newuser.subscribed = True;
    else: newuser.subscribed = False;
    if(number != ""): newuser.number = number
    newuser.put()
    
def createPublicSubscribed(email):
    uemails = db.GqlQuery('SELECT * '
                       'FROM User '
                       'WHERE ANCESTOR IS :1 AND email = :2',
                       UserTable_key(), email)
    pemails = findPublicEmail(email)
    if(uemails.count() != 0 | pemails.count()): return
    sub = publicSubscribed(parent=UserTable_key())
    sub.email = email
    sub.put()
    
def getSubscribed():
    return db.GqlQuery('SELECT email '
                                  'FROM User '
                                  'WHERE ANCESTOR IS :1 AND subscribed = true ',
                                  UserTable_key())
def getPublicSubscribed():
    return db.GqlQuery('SELECT email '
                                         'FROM publicSubscribed '
                                         'WHERE ANCESTOR IS :1 ',
                                         UserTable_key())

    
def findPublicEmail(email):
    return db.GqlQuery('SELECT * '
                       'FROM publicSubscribed '
                       'WHERE ANCESTOR IS :1 AND email = :2',
                       UserTable_key(), email)