from enums import AuthorisationLevels
from datetime import datetime
import settings
import bcrypt

class DataBaseError(Exception):
    pass

class DataBase(object):
    def __init__(self, connection_string):
        """
        This is called when the database is connected to. The connection
        string parameter is the string configured in settings.py and
        should be used to access the database.
        :param connection_string:a string used to find and access the
         database.
        """
        raise NotImplementedError()
        
    def get_post_by_id(self, id_val):
        """
        Used to retreive a post from an id associated with that post in
        your database. This is most useful when trying to access
        non-published items.
        :param id_val:any value that uniquely identifies a post
        Returns a Post object
        """
        raise NotImplementedError()
        
    def get_all_posts(self):
        """
        A catch-all used to return every post in the database. Usually
        used to find non-published posts.
        Returns an iterable full of Post objects.
        """
        raise NotImplementedError()

    def get_published_post(self, year, month, post_name):
        """
        Returns a post that has been published. Used most often for
        individual blog posts being viewed.
        :param year:a year integer for that post.
        :param month:a month integer for that post.
        :param post_name:the unique name for that year/month combo.
        Returns Post object.
        """
        raise NotImplementedError()
    
    def get_published_posts(self, year=None, month=None, page=None):
        """
        Returns a list of posts that have been published. Used most
        often for the front page, but also archives.
        The year and month param are optional to limit results from just
        the archives if required. With neither specified it returns the
        front page results.
        :param year:a year integer for that post.
        :param month:a month integer for that post.
        :param post_name:the unique name for that year/month combo.
        Returns Post object.
        """
        raise NotImplementedError()
        
    def add_post(self, post):
        """
        Takes a fully formatted Post object and stores it in the
        database.
        :param post:a Post object to save.
        Returns completed post object (with id)
        """
        raise NotImplementedError()

    def get_user(self, user):
        """
        Takes a username and returns a User object populated from the
        database entry.
        :param user:username used to uniquely identify user.
        """
        raise NotImplementedError()
        
    def add_user(self, user):
        """
        Takes a User object and stores it in the database.
        It will have to check it's unique constraints.
        :param user:User object to store.
        """
        raise NotImplementedError()
        
    def get_page(self, name):
        """
        Takes the page name and returns a Page object populated from the
        database entry.
        :param name:used to uniquely identify the page.
        """
        raise NotImplementedError()
        
    def add_page(self, name):
        """
        Takes a page name and returns a Page object populated from the
        database entry.
        :param name:used to uniquely identify the page.
        """
        raise NotImplementedError()
        
    def get_all_pages(self):
        """
        A catch-all used to return every page in the database. Usually
        used to find non-published pages.
        Returns an iterable full of Page objects.
        """
        raise NotImplementedError()
        
        
class Item(object):
    """
    A base blog post. Could turn in to a comment, blog entry or podcast episode just by extending it.
    """
    def __init__(self, content, user, updated, published):
        """
        :param content:the content of your entry.
        :param user:the user object this item was created by.
        :param updated:a datetime object of when this entry was last updated.
        """
        self.content = content
        self.user = user
        self.updated = updated
        self.published = published
        
class Comment(Item):
    """
    A comment object that holds comments for an item.
    """
    def __init__(self, content, user, post, updated, published):
        """
        :param post:a post object that this comment is the child of.
        """
        self.post = post
        super(Comment, self).__init__(content, user, updated, published)
        
class Page(Item):
    """
    Represents a blog entry.
    
    It is recommended you extend this object through inheritance so that
    you can more easily manipulate your database.
    """
    @classmethod
    def from_form(cls, form, user):
        """
        Accepts the WTForms Form object and a User object to turn in to
        a Post.
        """
        name = form.name.data
        content = form.content.data
        published = datetime.utcnow() if form.published.data else None
        updated = datetime.utcnow()
        return cls(name, content, user, updated, published)
            
    def __init__(self, name, content, user, updated, published):
        """
        :param name:the URL safe identifier of the page.
        """
        self.name = name
        super(Page, self).__init__(content, user, updated, published)
    
class Post(Page):
    """
    Represents a blog entry.
    
    It is recommended you extend this object through inheritance so that
    you can more easily manipulate your database.
    """
    @classmethod
    def from_form(cls, form, user):
        """
        Accepts the WTForms Form object and a User object to turn in to
        a Post.
        """
        id_val = form.id_val.data
        title = form.title.data
        name = title.replace(" ", "-").lower()
        content = form.content.data
        published = datetime.utcnow() if form.published.data else None
        updated = datetime.utcnow()
        return cls(id_val, name, title, content, user, updated, published)
        
    def __init__(self, id_val, name, title, content, user, updated, published):
        """
        Same as page but uses an `id_val` (any value) to identify the post when
        it is not published.
        """
        self.id_val = id_val
        self.name = name
        self.title = title
        super(Post, self).__init__(name, content, user, updated, published)
        
class User(object):
    """
    Represents a user in the database.
    
    Be aware that it is required that you hash a users password before
    entering it in to the database. This is for very good security
    reasons in-case you ever had your database stolen. This technique
    will prevent the attackers from easily brute-forcing the passwords.
    
    It is recommended you extend this object through inheritance so that
    you can more easily manipulate your database.
    """
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
        
        
        
    
    
