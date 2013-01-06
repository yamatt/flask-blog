from base import DataBase, Post, User, Page, DataBaseError
import sqlite3
from datetime import datetime

class DataBase(DataBase):
    SETUP_COMMANDS = [
        """CREATE TABLE IF NOT EXISTS posts (name TEXT, title TEXT, content TEXT, updated INTEGER, published INTEGER, user TEXT)""",
        """CREATE TABLE IF NOT EXISTS users (username TEXT, fullname TEXT, email TEXT, hashed_password BLOB, authorisation_level INTEGER, PRIMARY KEY(username))""",
        """CREATE TABLE IF NOT EXISTS pages (name TEXT, title TEXT, content TEXT, updated INTEGER, published INTEGER, user TEXT)""",
    ]

    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cursor = self.conn.cursor()
        for command in self.SETUP_COMMANDS:
            self.cursor.execute(command)
        self.conn.commit()
        
    def get_post_by_id(self, id_val):
        REQUEST = """SELECT rowid, name, title, content, user, updated, published FROM posts WHERE (rowid=?)"""
        result = self.cursor.execute(REQUEST, [id_val]).fetchone()
        if result:
            return Post.from_result(self, result)
        
    def get_all_posts(self):
        REQUEST = """SELECT rowid, name, title, content, user, updated, published FROM posts"""
        results = []
        for row in self.cursor.execute(REQUEST):
            post = Post(*row)
            results.append(post)
        return results

    def get_published_post(self, year, month, post_name):
        REQUEST = """SELECT rowid, name, title, content, user, updated, published FROM posts WHERE (published > ? AND published < ? AND name = ?)"""
        
        dt_start = datetime(year, month, 1)
        epoc_start = int(dt_start.strftime("%s"))
        month += 1
        if month > 12:
            year = year + 1
            month = 1
        dt_end = datetime(year, month, 1)
        epoc_end = int(dt_end.strftime("%s"))
        
        result = self.cursor.execute(REQUEST, [epoc_start, epoc_end, post_name]).fetchone()
        if result:
            return Post.from_result(self, result)
    
    def get_published_posts(self, year=None, month=None, page=None):
        REQUEST_DATE = """SELECT rowid, name, title, content, user, updated, published FROM posts WHERE (published > ? AND published < ?)"""
        REQUEST = """SELECT rowid, name, title, content, user, updated, published FROM posts WHERE (published > 0)"""
        
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
                post = Post.from_result(self, row)
                results.append(post)
        else:
            # get all
            for row in self.cursor.execute(REQUEST):
                post = Post.from_result(self, row)
                results.append(post)
            
        return results
        
    def add_post(self, post):
        data = post.to_row()
        row_id = post.id_val
        if row_id:
            #update
            REQUEST = """UPDATE posts SET name=?, title=?, content=?, updated=?, published=?, user=? WHERE (rowid = ?);"""
            data += tuple(row_id,)
            self.cursor.execute(REQUEST, data)
        else:
            #new
            REQUEST = """INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)"""
            self.cursor.execute(REQUEST, data)
            row_id  = self.cursor.lastrowid
        self._save()
        return self.get_post_by_id(row_id)

    def get_user(self, user):
        REQUEST = """SELECT username, fullname, email, hashed_password, authorisation_level FROM users WHERE (username = ?)"""
        result = self.cursor.execute(REQUEST, (user,)).fetchone()
        if result:
            return User(*result)
        
    def add_user(self, user):
        REQUEST = """INSERT INTO users VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(REQUEST, user.to_row())
        self._save()
        
    def get_page(self, name):
        REQUEST = """SELECT rowid, name, title, content, updated, published, user FROM pages WHERE (name=?)"""
        result = self.cursor.execute(REQUEST, (name,)).fetchone()
        if result:
            return Page.from_result(self, result)
        
    def add_page(self, page):
        data = page.to_row()
        exists = bool(self.get_page(page.name))
        if exists:
            #update
            REQUEST = """UPDATE pages SET name=?, title=?, content=?, updated=?, published=?, user=?  WHERE (name = ?);"""
            data += (page.name,)
            self.cursor.execute(REQUEST, data)
        else:
            #new
            REQUEST = """INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?)"""
            self.cursor.execute(REQUEST, data)
        self._save()
        
    def get_all_pages(self):
        REQUEST = """SELECT name, content, user, updated, published FROM pages"""
        results = []
        for row in self.cursor.execute(REQUEST):
            page = Page(*row)
            results.append(page)
        return results
        
    def delete_page(self, name):
        REQUEST = """DELETE FROM pages WHERE name=?"""
        self.cursor.execute(REQUEST, (name,))
        self._save()
        
    def _save(self):
        self.conn.commit()

class Post(Post):
    @classmethod
    def from_result(cls, database, result):
        id_val = result[0]
        name = result[1]
        title = result[2]
        content = result[3]
        user = database.get_user(result[4])
        updated = datetime.fromtimestamp(result[5])
        published = result[6]
        if published:
            published = datetime.fromtimestamp(published)
        return cls(id_val, name, title, content, user, updated, published)
        
    def to_row(self):
        updated = int(datetime.utcnow().strftime("%s"))
        if self.published:
            published = int(self.published.strftime("%s"))
        else:
            published = self.published
        return (self.name, self.title, self.content, updated, published, self.user.username)

class User(User):
    def to_row(self):
        return (self.username, self.fullname, self.email, self.hashed_password, self.authorisation_level)
        
class Page(Page):
    @classmethod
    def from_result(cls, database, result):
        id_val = result[0]
        name = result[1]
        title = result[2]
        content = result[3]
        updated = datetime.fromtimestamp(result[4])
        published = result[5]
        user = database.get_user(result[6])
        if published:
            published = datetime.fromtimestamp(published)
        return cls(id_val, name, content, user, updated, published)
        
    def to_row(self):
        updated = int(datetime.utcnow().strftime("%s"))
        if self.published:
            published = int(self.published.strftime("%s"))
        else:
            published = self.published
        return (self.name, self.title, self.content, updated, published, self.user.username)
