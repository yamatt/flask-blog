from flask import Flask, request, url_for,g , session, flash, redirect, render_template
from models.couchdb import DataBase
import settings
from enums import AuthorisationLevels
app = Flask(__name__)
app.config.from_object(settings)

def is_admin(fn, user_level=AuthorisationLevels.ADMIN):
    def wrap():
        username = session.get('username')
        if username:
            user = g.db.get_user(username)
            if user['level'] => user_level:
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
    g.db = DataBase(app.config['CONNECTION'], app.config['TABLE'], app.config['USERNAME'], app.config['PASSWORD'], per_page=app.config['PER_PAGE'])

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
@app.route('/posts/new', method=["GET", "POST"])
@app.route('/posts/<int:year>/<int:month>/<post_name>/edit', method=["GET", "POST"])
def change():
    """
    Edit or add a new post
    """
    


@app.route('/login', method=["GET", "POST"])
def login():
    if not session.get("username"):
        if request.method == "POST":
            username = request.form['username'] # wtforms pls
            password = request.form['password']
            remember = request.form['remember']
            if g.db.is_user(username, password):
                session['username'] = username
                if remember == "yes":
                    session.permanent = True
                flash("You are now logged in.")
                return redirect(for_url("posts")
            else:
                flash("Could not log you in with that username and password combination. Please try again.")
        return render_template('login.jinja.html')
    else:
        flash("You are already logged in.")
        return redirect(for_url("posts"))

@app.route('/config', method=["GET", "POST"])
def config():
    pass

if __name__ == '__main__':
    app.run()
    app.permanent_session_lifetime = timedelta(**app.config['PERMINENT_LOGON_TIMEOUT'])
