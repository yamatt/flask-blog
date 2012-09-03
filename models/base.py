from datetime import datetime
from enums import AuthorisationLevels
import settings
import bcrypt

class DataBaseError(Exception):
    pass

class DataBase(object):

    def __init__(self, connection_string):
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
        
    def get_post_by_id(self, id_val):
        """
        Return a post from the id.
        """
        raise NotImplementedError()
        
    def get_posts(self, year=None, month=None, page=None):
        """
        Return a list of Post objects that match the parameters.
        """
        raise NotImplementedError()
        
    def get_published_posts(self, page=None):
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
        
    def update_user(self, user):
        raise NotImplementedError()
        
        
class Item(object):
    """
    A base blog post. Could turn in to a comment, blog entry or podcast episode just by extending it.
    """
    def __init__(self, content, user, updated=None):
        """
        @param content: the content of your entry.
        @param user: the user object this item was created by.
        @param created: a datetime object of when this entry was created.
        """
        self.content = content
        self.user = user
        self.updated = updated
        if not updated:
            self.updated = datetime.utcnow()
        
class Comment(Item):
    """
    A comment object that holds comments for an item.
    """
    def __init__(self, content, user, post, updated=None):
        """
        @param post: a post object that this comment is the child of.
        """
        self.post = post
        super(Comment, self).__init__(content, user, created)
        
class Page(Item):        
    def __init__(self, name, title, content, user, published=False):
        self.name = name
        self.published = None
        if published:
            self.published = datetime.utcnow()
        super(Page, self).__init__(content, user)
    
class Post(Page):
    """
    A post object that represents a new post.
    """
    @classmethod
    def from_form(cls, form, user):
        id_val = form.id_val.data
        title = form.title.data
        content = form.content.data
        user = user
        published = form.published.data
        return cls(id_val, title, content, user, published)
        
    def __init__(self, id_val, title, content, user, updated=None, published=False):
        self.id_val = id_val
        self.title = title
        name = title.replace(" ", "-")
        super(Post, self).__init__(name, title, content, user, published)
        
        
class User(object):
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def __init__(self, username, fullname, email, hashed_password, authorisation_level=AuthorisationLevels.COMMENTOR):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.hashed_password = hashed_password
        self.authorisation_level = authorisation_level
        
    def password_matches(self, password):
        return bcrypt.hashpw(password, self.hashed_password) == self.hashed_password
        
        
        
    
    
