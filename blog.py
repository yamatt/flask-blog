from flask import Flask, request, url_for,g , session, flash, redirect, render_template
import settings
from enums import AuthorisationLevels
from models.forms import Login
from datetime import timedelta

def create_database():
    global database
    database_name = ".".join(["models", settings.DATABASE_TYPE])
    database_module = __import__(database_name, globals(), locals(), [])
    database = getattr(database_module, settings.DATABASE_TYPE)
create_database()

app = Flask(__name__)
app.config.from_object(settings)

def is_admin(fn, user_level=AuthorisationLevels.ADMIN):
    def wrap():
        username = session.get('username')
        if username:
            user = g.db.get_user(username)
            if user['level'] >= user_level:
                return fn()
            else:
                flash("You are not authenticated for this action.")
                return url_for('posts')
        else:
            flash("You are not logged in.")
            return url_for('login')

@app.before_first_request
def setup_database_connection():
    """
    Creates database objects
    """
    g.db = database.DataBase(app.config['CONNECTION'])

@app.route('/')
@app.route('/posts/')
@app.route('/posts/<int:year>')
@app.route('/posts/<int:year>/<int:month>')
def posts(year=None, month=None, post_name=None):
    """
    Handles display of all posts including front page and archived.
    """
    page = request.args.get('page')
    if page:
        page = int(page) * int(app.config['PER_PAGE'])
    if year:
        posts = g.db.get_posts_by_date(year=year, month=month, page=page)
    else:
        posts = g.db.get_latest_posts(page=page)
    return render_template('posts.jinja.html', posts=posts)

@app.route('/posts/<int:year>/<int:month>/<post_name>')
def post(year=None, month=None, post_name=None):
    post = g.db.get_post(year=year, month=month, post_name=post_name)
    render_template('post.mark.html', post=post)

@is_admin
@app.route('/posts/new', methods=["GET", "POST"])
@app.route('/posts/<int:year>/<int:month>/<post_name>/edit', methods=["GET", "POST"])
def change():
    """
    Edit or add a new post
    """


@app.route('/login', methods=["GET", "POST"])
def login():
    if not session.get("username"):
        form = Login()
        if form.validate_on_submit():
            user = g.db.get_user(form.username.data)
            if user.password_matches(form.password.data):
                session['username'] = user.username
                flash("Logged in successfully")
                return redirect(for_url("posts"))
            else:
                flash("That username and password combination could not be found.")
        return render_template('login.jinja.html', form=form)
    else:
        flash("""You are already logged in. <a href="%s">Logout?</a>""" % for_url("logout"))
        return redirect(for_url("posts"))
        
@app.route('/logout')
def logout():
    session.pop("username")
    flash("""You have been logged out. <a href="">Login?</a>""" % for_url("login"))
    return redirect(for_url("posts"))

@app.route('/config', methods=["GET", "POST"])
def config():
    pass

if __name__ == '__main__':
    app.permanent_session_lifetime = timedelta(**app.config['PERMANENT_LOGON_TIMEOUT'])
    app.run()
