#!/usr/bin/env python2
from flask.ext.script import Manager, prompt_pass

import sys

from enums import AuthorisationLevels

import app

manager = Manager(app.app)

def create_database():
    app.database.engine.create()

def create_admin(username, password, full_name="Administrator", e_mail=""):
    hashed_password = app.database.models.User.hash_password(password)
    user = app.database.models.User(username, full_name, e_mail, hashed_password, AuthorisationLevels.ADMIN)
    app.database.engine.add_user(user)
    
def user_exists(username):
    user = app.database.engine.get_user(username)
    return bool(user)

@manager.command
def setupdb(username):
    create_database()
    
    if user_exists(username):
        print "This username already exists. Another one must be chosen."
        exit(1)
    else:
        password = prompt_pass("{0}'s password: ".format(username))
        password_confirm = prompt_pass("Confirm password: ")
        if password != password_confirm:
            print "Passwords do not match. Please try again."
            exit(1)
            
    create_admin(username, password)
    
if __name__ == "__main__":
    manager.run()

