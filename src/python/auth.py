import hashlib
import os
import logging
import string
from google.appengine.ext import db
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class User(db.Model):
    username = db.StringProperty()
    passwordHash = db.StringProperty()
    permissions = db.StringProperty()
    keyHash = db.StringProperty()
    
class authKey(db.Model):
    userKey = db.StringProperty()
    authKey = db.StringProperty()
    expirationDate = db.DateTimeProperty()
    
def UserTable_key():
    return db.Key.from_path('UserTableversion', 'UserTable1')

def KeyTable_key():
    return db.Key.from_path('KeyTableversion', 'KeyTable1')

class invalidLogon(Exception):
    pass

def authorize(key):
    keyhash = hashlib.md5(key).hexdigest()
    logging.info(keyhash)
    user = db.GqlQuery("SELECT * "
                           "FROM User "
                           "WHERE ANCESTOR IS :1 AND keyHash = :2 "
                           "Limit 1 ",
                           UserTable_key(), keyhash)[0]
    return user
    
def logIn(username, password):
    logging.info("Username = '%s'" % username)
    logging.info(UserTable_key())
    try:
        user = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE ANCESTOR IS :1 AND username = :2 "
                        "Limit 1 ",
                        UserTable_key(), username)[0]
    except IndexError:
        user = None
        
    if (user is None): 
        logging.info("user is none")
        raise(invalidLogon)
        
    logging.info("user.passwordHash is: '" + user.passwordHash + "' password is: '" + password + "' hashlib.md5(password).hexdigest() is " + hashlib.md5(password).hexdigest())
    if (user.passwordHash != hashlib.md5(password).hexdigest()): raise(invalidLogon)
    
    key = id_generator(16)
    h = hashlib.md5(key).hexdigest()
    user.keyHash = h
    user.put()
    return key

def createUser(username, password, permissions):
    newuser = User(parent=UserTable_key())
    newuser.username = username
    newuser.passwordHash = hashlib.md5(password).hexdigest()
    newuser.permissions = permissions
    newuser.put()