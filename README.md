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
The easiest way to get started is to first create a database with an administrator account. Run `create_admin.py` to setup the database like so:

    ./create_admin.py matt

Where matt is the username. It can be your own name if you prefer.

*Open up the `settings.py` file and change the `SECRET_KEY` to be anything non-guessable.*

Run the app do:

    ./main.py

And follow the directions to access the site from your browser.

# Tips
1. Going to `/accounts/login` will allow the admin account that was created to login.
1. Going to `/new` will allow you to create a new page. Pages are not posts. Pages are like the about page. If you create an about page the content will be displayed in the sidebar.
1. Going to `/posts/new` will allow you to create a new post.
1. `/list` and `/posts/list` will give you a list of pages and posts that have been created (even ones that weren't published).
1. A lot of configuration is stored in the `settings.py` file.

# Still to do
* Upload app
* Commenting
* User registration
* User editing
* Generic theme
* Mobile themes
* Redo login part to use Flask-Login
* Tests
