import unittest
from os import remove
from models import sqlite
from uuid import uuid4 as uuid
import sqlite3

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
        

if __name__ == "__main__":
    unittest.main()
