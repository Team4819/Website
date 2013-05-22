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
    
class publicUser(User):
    firstName = "Public"
    lastName = "User"
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
    logging.info(keyhash)
    try:
        user = db.GqlQuery("SELECT * "
                           "FROM User "
                           "WHERE ANCESTOR IS :1 AND keyHash = :2 "
                           "Limit 1 ",
                           UserTable_key(), keyhash)[0]
    except IndexError:
        user = publicUser
    return user
    
def logIn(firstName, lastName, password):
    logging.info("name = '%s'" % firstName + lastName)
    logging.info(UserTable_key())
    try:
        user = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE ANCESTOR IS :1 AND lcaseName = :2 "
                        "Limit 1 ",
                        UserTable_key(), str(firstName).lower() + " " + str(lastName).lower())[0]
    except IndexError:
        user = publicUser
        raise(invalidLogon)
        
        
    logging.info("user.passwordHash is: '" + user.passwordHash + "' password is: '" + password + "' hashlib.md5(password).hexdigest() is " + hashlib.md5(password).hexdigest())
    if (user.passwordHash != hashlib.md5(password).hexdigest()): raise(invalidLogon)
    
    key = id_generator(16)
    h = hashlib.md5(key).hexdigest()
    user.keyHash = h
    user.put()
    return key

def createUser(firstName, lastName, password, permissions):
    newuser = User(parent=UserTable_key())
    newuser.firstName = firstName
    newuser.lastName = lastName
    newuser.lcaseName = str(firstName).lower() + " " + str(lastName).lower()
    newuser.passwordHash = hashlib.md5(password).hexdigest()
    newuser.permissions = int(permissions)
    newuser.put()