import unittest
from os import remove
from models import sqlite
from uuid import uuid4 as uuid
import sqlite3
from datetime import datetime
from mockito import *

MockUser = mock()
MockUser.username = "test_user"


class TestSQLiteDB(unittest.TestCase):
    TEST_DB = "test.db"
    def setUp(self):
        self.blog_db = sqlite.DataBase(self.TEST_DB)
        self.norm_db_cur = sqlite3.connect(self.TEST_DB).cursor()
        
    def tearDown(self):
        remove(self.TEST_DB)
        
    def _add_user(self):
        password = sqlite.User.hash_password(uuid().hex)
        values = ("name", "full name", "email", password, 123)
        user = sqlite.User(*values)
        self.blog_db.add_user(user)
        return values
        
    def test_user_add(self):
        values = self._add_user()
        
        results = self.norm_db_cur.execute("SELECT username, fullname, email, hashed_password, authorisation_level FROM users")
        row = results.fetchone()
        self.assertNotEqual(row, None)
        self.assertEqual(row, values)
        
    def test_user_get(self):
        values = self._add_user()
        
        user = self.blog_db.get_user(values[0])
        self.assertEqual(user.to_row(), values)
        
    def test_posts(self):
        post_1 = sqlite.Post(None, "name1", "title1", "content1", MockUser, datetime.now(), datetime.now())
        post_2 = sqlite.Post(None, "name2", "title2", "content2", MockUser, datetime.now(), datetime.now())
        
        self.blog_db.add_post(post_1)
        self.blog_db.add_post(post_2)
        
        published_posts = self.blog_db.get_published_posts()
        
        self.assertEqual(len(published_posts), 2, "Failed. Found: {0}".format(published_posts))
        

if __name__ == "__main__":
    unittest.main()
