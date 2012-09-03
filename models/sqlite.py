from base import DataBase, Post, User, DataBaseError
import sqlite3
from datetime import datetime

class DataBase(DataBase):
    SETUP_COMMANDS = [
        """CREATE TABLE IF NOT EXISTS posts (name TEXT, title TEXT, content TEXT, updated INTEGER, published INTEGER, user TEXT)""",
        """CREATE TABLE IF NOT EXISTS users (username TEXT, fullname TEXT, email TEXT, hashed_password BLOB, authorisation_level INTEGER, PRIMARY KEY(username))"""
    ]

    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cursor = self.conn.cursor()
        for command in self.SETUP_COMMANDS:
            self.cursor.execute(command)
        self.conn.commit()
        
    def get_post_by_id(self, id_val):
        REQUEST = """SELECT rowid, title, content, user, updated, published FROM posts WHERE (rowid=?)"""
        result = self.cursor.execute(REQUEST, id_val).fetchone()
        return Post(*result)
        
    def get_all_posts(self):
        REQUEST = """SELECT rowid, title, content, updated, published, user FROM posts"""
        results = []
        for row in self.cursor.execute(REQUEST):
            post = Post(*row)
            results.append(post)
        return results

    def get_published_post(self, year, month, post_name):
        REQUEST = """SELECT rowid, title, content, updated, published, user FROM posts WHERE (published > ? AND published < ? AND name = ?)"""
        
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
    
    def get_published_posts(self, year=None, month=None, page=None):
        REQUEST_DATE = """SELECT title, content, user, created, published FROM posts WHERE (published > ? AND published)"""
        REQUEST = """SELECT title, content, updated, published, user FROM posts WHERE (published IS NOT NULL)"""
        
        def datetime_to_epoc(dt):
            return int(dt.strftime("%s"))
        
        results = []
        
        if year or month:
            if year and month:
                dt_start = datetime(year, month, 1)
                epoc_start = datetime_to_epoc(dt_start)
                month += 1
                if month > 12:
                    year = year + 1
                    month = 1
                dt_end = datetime(year, month, 1)
                epoc_end = int(dt_end.strftime("%s"))
            else:
                dt_start = datetime(year, 1, 1)
                epoc_start = int(dt_start.strftime("%s"))
                year += 1
                dt_end = datetime(year, 1, 1)
                epoc_end = int(dt_end.strftime("%s"))
                
            for row in self.cursor.execute(REQUEST_DATE, [epoc_start, epoc_end]):
                post = Posts(*row)
                results.append(post)
        else:
            # get all
            for row in self.cursor.execute(REQUEST):
                post = Post(None, row[0], row[1], self.get_user(row[2]), row[3], row[4])
                results.append(post)
            
        return results
        
    def _save(self):
        self.conn.commit()
        
    def add_post(self, post):
        data = (post.name, post.title, post.content, datetime.utcnow(), post.published, post.user.username)
        if post.id_val:
            #update
            """UPDATE posts SET (?, ?, ?, ?, ?, ?, ?) WHERE rowid = ?"""
            self.cursor.execute(REQUEST, data + (post.id_val))
        else:
            #new
            REQUEST = """INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)"""
            self.cursor.execute(REQUEST, data)
        self._save()

    def get_user(self, user):
        REQUEST = """SELECT username, fullname, email, hashed_password, authorisation_level FROM users WHERE (username = ?)"""
        result = self.cursor.execute(REQUEST, [user]).fetchone()
        if result:
            return User(*result)
        
    def add_user(self, user):
        REQUEST = """INSERT INTO users VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(REQUEST, user.to_row())
        self._save()


