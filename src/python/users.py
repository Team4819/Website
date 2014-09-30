import hashlib
import logging
import string
from google.appengine.ext import db
import random
import publicSubscribed


class User(db.Model):
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    fullName = db.StringProperty()
    lcaseName = db.StringProperty()
    passwordHash = db.StringProperty()

    #Permissions key:
    # 0: Public Restricted
    # 1: Read-only Member, can read restricted content
    # 2: Read-Write Member, can create and edit content, but only if he/she created it
    # 3: Admin, can read, create, and edit everything

    #TODO Remove this, groups are enough now
    permissions = db.IntegerProperty()

    groups = db.StringProperty()
    keyHash = db.StringProperty()
    email = db.EmailProperty()

    #TODO This can also be done better with groups
    subscribed = db.BooleanProperty()

    number = db.PhoneNumberProperty()

    def isGroup(self, group):
        if self.groups is not None:
            split = self.groups.split(",")
            [x.strip().lower() for x in split]
            if group.strip().lower() in split:
                return True
            else:
                return False
        else:
            return False


class publicUser(User):
    firstName = "Public"
    lastName = "User"
    fullname = "Public User"
    groups = "public"
    subscribed = False
    permissions = 0

currentUser = publicUser()


def db_key():
    return db.Key.from_path('UserTable-version', 'UserTable-1')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class authKey(db.Model):
    userKey = db.StringProperty()
    authKey = db.StringProperty()
    expirationDate = db.DateTimeProperty()

class invalidLogon(Exception):
    pass

class noSuchUser(Exception):
    pass


def create_user(firstName, lastName, email, number, password):
    newuser = User(parent=db_key())
    newuser.firstName = firstName
    newuser.lastName = lastName
    newuser.fullName = firstName + " " + lastName
    newuser.lcaseName = str(firstName).lower() + " " + str(lastName).lower()
    newuser.passwordHash = hashlib.md5(password).hexdigest()
    newuser.permissions = 1
    newuser.teamStatus = 1
    newuser.email = email
    pemail = publicSubscribed.findPublicEmail(email)
    if pemail.count() != 0:
        pemail[0].delete()
    newuser.subscribed = True
    if number != "":
        newuser.number = number
    newuser.groups = "public"
    newuser.put()


def get_session(request):
    global currentUser
    if(request.cookies.get("LoginStatus") == "LoggedIn"):
        currentUser = authorize(request.cookies.get("authKey"))
    else:
        currentUser = publicUser()


def authorize(key):
    keyhash = hashlib.md5(key).hexdigest()
    try:
        user = db.GqlQuery("SELECT * "
                            "FROM User "
                            "WHERE ANCESTOR IS :1 AND keyHash = :2 "
                            "Limit 1 ",
                            db_key(), keyhash)[0]
    except IndexError:
        user = publicUser()
    if user.subscribed is None:
        user.subscribed = False
        user.put()
    return user


def log_in(firstName, lastName, password):
    try:
        user = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE ANCESTOR IS :1 AND lcaseName = :2 "
                        "Limit 1 ",
                        db_key(), str(firstName).lower() + " " + str(lastName).lower())[0]
    except IndexError:
        user = publicUser
        raise invalidLogon

    if user.passwordHash != hashlib.md5(password).hexdigest(): raise(invalidLogon)

    key = id_generator(16)
    h = hashlib.md5(key).hexdigest()
    user.keyHash = h
    user.put()
    return key


def lookupEmail(email):
    emails = getAllEmails()
    logging.info("looking up " + email)
    for adress in emails:
        logging.info("checking adress " + adress.email)
        if adress.email in email:
            logging.info("success!!")
            return db.GqlQuery('SELECT * '
                               'FROM User '
                               'WHERE ANCESTOR IS :1 AND email = :2',
                               db_key(), adress.email)
    return db.GqlQuery('SELECT * '
                       'FROM User '
                       'WHERE ANCESTOR IS :1 AND email = :2',
                       db_key(), email )


def getAllEmails():
    return db.GqlQuery('SELECT email '
                       'FROM User '
                       'WHERE ANCESTOR IS :1 AND email != NULL ',
                       db_key())


def refreshAll():
    users = db.GqlQuery("SELECT * "
                           "FROM User "
                           "WHERE ANCESTOR IS :1",
                           db_key())
    for user in users:
        user.subscribed = True
        user.put()
