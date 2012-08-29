from couchdb import Server
from datetime import datetime
from enums import AuthorisationLevels
import settings
import bcrypt

class DataBaseError(Exception):
    pass

class DataBase(object):
    @classmethod
    def setup(cls):
        return cls(settings.CONNECTION, settings.TABLE, settings.USERNAME, settings.PASSWORD)

    def __init__(self):
        """
        Set up all your database server connection here.
        """
        raise NotImplementedError()
        
    def get_post(self, year=None, month=None, post_name=None):
        """
        Return a complete Post object that matches the parameters.
        @param year: an integer year value for the year the post was published.
        """
        raise NotImplementedError()
        
    def get_posts(self, year=None, month=None, page=None):
        """
        Return a list of Post objects that match the parameters.
        """
        raise NotImplementedError()
        
    def get_latest_posts(self, page=None):
        """
        Return array of items for front page
        """
        raise NotImplementedError()
        
    def add_post(self, post):
        raise NotImplementedError()
        
    def get_user(self, user):
        raise NotImplementedError()
        
    def add_user(self, user):
        raise NotImplementedError()
        
        
class Item(object):
    """
    A base blog post. Could turn in to a comment, blog entry or podcast episode just by extending it.
    """
    def __init__(self, content, user, created=None):
        """
        @param content: the content of your entry.
        @param user: the user object this item was created by.
        @param created: a datetime object of when this entry was created.
        """
        self.content = content
        self.user = user
        self.created = created if created else datetime.now()
        
class Comment(Item):
    """
    A comment object that holds comments for an item.
    """
    type = "comment"
    def __init__(self, content, user, post, created=None):
        """
        @param post: a post object that this comment is the child of.
        """
        self.post = post
        super(Comment, self).__init__(content, user, created)
    
class Post(Item):
    """
    A post object that represents a new post.
    """
    type = "post"
    
    def __init__(self, title, content, user, created=None, published=False):
        self.title = title
        self.published = datetime.now() if published else None
        super(Post, self).__init__(content, user, created)
        
        
class User(object):
    type = "user"
    
    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    def __init__(self, username, hashed_password, authorisation_level=AuthorisationLevels.COMMENTOR):
        self.username = username
        self.hashed_password = hashed_password
        self.authorisation_level = authorisation_level
        
    def password_matches(self, password):
        return bcrypt.hashpw(password, self.hashed_password) == self.hashed_password
        
        
        
    
    
