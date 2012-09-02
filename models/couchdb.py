from couchdb import Server
from datetime import datetime
from enums import AuthorisationLevels
import settings
from base import DataBase, Post, User, DataBaseError
from urlparse import urlparse
try:
    from json import dumps as jsonsdump
except ImportError:
    from simplejson import dumps as jsonsdump

class DataBase(object):
    DESIGN_NAME = "_design/blog"
    DESIGN_CONTENTS = {
        "views": {
            "post": {
                "map": """function(doc) {
                            if (doc.type=="post") {
                                emit((doc.published[0], doc.published[1], doc.title), doc)
                            }
                        }
                    """
            },
            "posts": {
                "map": """function(doc) {
                            if (doc.type=="post") {
                                emit((doc.created), doc)
                            }
                        }
                    """
            },
            "posts-published": {
                "map": """function(doc) {
                            if ((doc.type=="post") &&(doc.published != null) ) {
                                emit((doc.published), doc)
                            }
                        }
                    """
            },
            "user": {
                "map": """function(doc) {
                            if (doc.type=="user") {
                                emit(doc.username, doc)
                            }
                        }
                    """
                }
            }
        }

    def __init__(self, connection_string):
        """
        Detect state of database and create if nessecery.
        """
        url = urlparse(connection_string)
        server_url = "http://%s:%s" % (url.hostname, url.port)
        self.server = Server(server_url)
        if url.username and url.password:
            self.server.resource.credentials = (url.username, url.password)
        table_name = url.path[1:]
        self.db = self.server.get(table_name)
        if not self.db:
            self.db = self.server.create(table_name)
            self.db[self.DESIGN_NAME] = self.DESIGN_CONTENTS
        
    def _return_view(self, view_name, key=None, key_start=None, key_end=None, descending=False):
        path = self.DESIGN_NAME + "/_view/" + view_name
        params = dict()
        if key:
            params.update({"key": key_start})
        elif key_start and key_end:
            params.update({"startkey": key_start})
            params.update({"endkey": key_end})

        if descending:
            params.update({"descending", "true"})
            
        results = db.view(path, params)
        return results.rows
        
    def get_post(self, year, month, post_name):
        """
        Return a complete Post object that matches the parameters.
        @param year: an integer year value for the year the post was published.
        """
        key = jsonsdump([year, month, post_name])
        results = self._return_view("post", key=key)
        if len(results):
            return self._row_to_post(results[0])
        raise DataBaseError("No results found for this key.")
        
    def get_posts(self, year, month=None, page=None):
        """
        Return a list of Post objects that match the parameters.
        """
        if year and month:
            key_start = [year, month, 1, 0, 0, 0]
            key_end = [year, month, 32, 0, 0, 0] # a little hack to get all entries specified month
        elif year:
            key_start = [year, 1, 1, 0, 0, 0]
            key_end = [year, 13, 0, 0, 0, 0] # a little hack to get all entries specified year
        rows = self._return_view("posts", key_start=key_start, key_stop=key_stop)
        posts = []
        for row in rows:
            post = Posts.from_row(row)
            posts.append(post)
        return posts
        
    def get_published_posts(self, year=None, month=None, page=None):
        """
        Return array of published items
        """
        if year and month:
            key_start = [year, month, 1, 0, 0, 0]
            key_end = [year, month, 32, 0, 0, 0] # a little hack to get all entries specified month
        elif year:
            key_start = [year, 1, 1, 0, 0, 0]
            key_end = [year, 13, 0, 0, 0, 0] # a little hack to get all entries specified year
        else:
            key_start = None
            key_end = None
        rows = self._return_view("posts-published", key_start=key_start, key_stop=key_stop)
        posts = []
        for row in rows:
            post = Posts.from_row(row)
            posts.append(post)
        return posts
        
    def add_post(self, post):
        db.save(dict(post))
        
    def get_user(self, user):
        rows = self._return_view("user", key=user)
        if len(row):
            return User.from_row(row[0])
        raise DataBaseError("No results found for this user.")
        
    def add_user(self, user):
        db.save(dict(user))
        
class Post(Post):
    type = "post"
    @classmethod
    def from_row(cls, row):
        post = row['value']
        user = User.from_username(post['user'])
        created = datetime(*post['created'])
        published = post['published']
        if published:
            published = datetime(*published)
        return cls(title=post['title'], content=post['content'], user=user, created=created, published=published)
        
    def __dict__(self):
        return self.__dict__
        
class User(User):
    type = "user"
    @classmethod
    def from_row(cls, row):
        user = row['value']
        return cls(user.username, fullname, email, user.hashed_password, user.authorisation_level)

    def __dict__(self):
        return self.__dict__
