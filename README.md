# Flask-Blog
This is a blog I built to run in Python using the Flask micro-web framework.

# Requirements
* Python >=2.6
* python-flask >=0.8 (maybe 0.7 too)
* python-wtforms
* flask-WTF (from PyPI)
* python-sqlite (if you're using sqlite)
* python-bcrypt (for password hashes)

# Setup
Copy the `settings.py.defaults` file to `settings.py` and open it to set your preferences.
**Change the `SECRET_KEY` to be anything non-guessable.**

The easiest way to get started is to first create a database with an administrator account. Run `create_db.py` to setup the database like so:

    ./create_db.py Administrator

Where matt is the username for the administrative account you want to known by. It can be your own name if you prefer. You will then be asked to set up a password for this account.

To run the blog as a demonstration do:

    ./main.py

And follow the directions to access the site from your browser.

**However** if you want to run the blog on a public website please follow instructions on setting it up with a proper HTTP server such as Apace or Nginx and uWSGI.

# Tips
1. Going to `/accounts/login` will allow the admin account that was created to login.
1. Going to `/new` will allow you to create a new page. Pages are not posts. Pages are like the about page. If you create an about page the content will be displayed in the sidebar.
1. Going to `/posts/new` will allow you to create a new post.
1. `/list` and `/posts/list` will give you a list of pages and posts that have been created (even ones that weren't published).
1. A lot of configuration is stored in the `settings.py` file.

# Still to do
* ~~Upload app~~
* Commenting
* User registration
* User editing
* Generic theme
* Mobile themes
* Redo login part to use Flask-Login
* Tests
* ~~Page titles~~
* ~~WAI testing~~
