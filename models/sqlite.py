from base import DataBase, Post, User, DataBaseError
import sqlite3
from datetime import datetime

class DataBase(DataBase):
    SETUP_COMMANDS = [
        """CREATE TABLE IF NOT EXISTS posts (title TEXT, content TEXT, created INTEGER, published INTEGER, user INTEGER)"""
        """CREATE TABLE IF NOT EXISTS users (username TEXT, fullname TEXT, email TEXT, hashed_password BLOB, authorisation_level INTEGER, PRIMARY KEY(username, ASC))"""
    ]

    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cursor = self.conn.cursor()
        for command in self.SETUP_COMMANDS:
            self.cursor.execute(command)

    def get_post(self, year, month, post_name):
        REQUEST = """SELECT id, title, content, created, published, user FROM posts WHERE (created > ? AND created < ? AND title = ?)"""
        
        dt_start = datetime(year, month, 1)
        epoc_start = int(dt_start.strftime("%s"))
        month += 1
        if month > 12:
            year = year + 1
            month = 1
        dt_end = datetime(year, month, 1)
        epoc_end = int(dt_end.strftime("%s"))
        
        result = self.cursor.execute(REQUEST, [epoc_start, epoc_end, post_name]).fetchone()
        
        return Post(*result)
        
    def get_posts(self, year, month=None, page=None):
        REQUEST = """SELECT id, title, content, created, published, user FROM posts WHERE (created > ? AND created < ?)"""
        
        dt_start = datetime(year, month, 1)
        epoc_start = int(dt_start.strftime("%s"))
        month += 1
        if month > 12:
            year = year + 1
            month = 1
        dt_end = datetime(year, month, 1)
        epoc_end = int(dt_end.strftime("%s"))
        
        results = []
        for row in self.cursor.execute(REQUEST, [epoc_start, epoc_end, post_name]):
            post = Posts(*row)
            results.append(post)
            
        return results
    
    def get_published_posts(self, year=None, month=None, page=None):
        REQUEST = """SELECT id, title, content, created, published, user FROM posts WHERE (created > ? AND created < ? AND published > 0)"""
        
        dt_start = datetime(year, month, 1)
        epoc_start = int(dt_start.strftime("%s"))
        month += 1
        if month > 12:
            year = year + 1
            month = 1
        dt_end = datetime(year, month, 1)
        epoc_end = int(dt_end.strftime("%s"))
            
        results = []
        for row in self.cursor.execute(REQUEST, [epoc_start, epoc_end, post_name]):
            post = Posts(*row)
            results.append(post)
            
        return results
        
    def add_post(self, post):
        REQUEST = """INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(REQUEST, post.to_row())

    def get_user(self, user):
        REQUEST = """SELECT username, fullname, email, hashed_password, authorisation_level FROM users WHERE (username = ?)"""
        return User(self.cursor.execute(REQUEST, [user]).fetchone())
        
    def add_user(self, user):
        REQUEST = """INSERT INTO user VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(REQUEST, user.to_row())

class Post(Post):
    def to_row(self):
        return (self.title, self.content, self.created, self.published, self.user.username)
        
class User(User):
    def to_row(self):
        return (self.username, self.fullname, self.email, self.hashed_password, self.authorisation_level)
