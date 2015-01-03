#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  create_admin.py
#  
#  Copyright 2013 Matthew Copperwaite <copperwaitem@01wubuntu01>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
from getpass import getpass

import settings
from models.interface import DatabaseInterface
from enums import AuthorisationLevels

database = DatabaseInterface(settings.DATABASE_ENGINE, settings.DATABASE_CONNECTION_STRING)

def create_database():
    database.engine.create()

def create_admin(username, password, full_name="Administrator", e_mail=""):
    hashed_password = database.models.User.hash_password(password)
    user = database.models.User(username, full_name, e_mail, hashed_password, AuthorisationLevels.ADMIN)
    database.engine.add_user(user)
    
def user_exists(username):
    user = database.engine.get_user(username)
    return bool(user)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "You must specify a username as the first argument."
        exit(1)
    else:
        create_database()
        username = sys.argv[1]
        if user_exists(username):
            print "This username already exists. Another one must be chosen."
            exit(1)
        if len(sys.argv) > 2:
            password = sys.argv[2]
        else:
            password = getpass("{0}'s password: ".format(username))
            password_confirm = getpass("Confirm password: ")
            if password != password_confirm:
                print "Passwords do not match. Please try again."
                exit(1)
                
        create_admin(username, password)
        exit
            

