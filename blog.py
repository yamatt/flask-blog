from flask import Flask, request, url_for, g , session, flash, redirect, render_template
import settings
from enums import AuthorisationLevels
from models.forms import Login, Post
from datetime import timedelta

def create_database():
    global database
    database_name = ".".join(["models", settings.DATABASE_TYPE])
    database_module = __import__(database_name, globals(), locals(), [])
    database = getattr(database_module, settings.DATABASE_TYPE)
create_database()

app = Flask(__name__)
app.config.from_object(settings)

def get_user():
    username = session.get('username')
    if username:
        user = g.db.get_user(username)
        return user

def is_admin(fn, user_level=AuthorisationLevels.ADMIN):
    def wrap():
        user = get_user()
        if username:
            if user['level'] >= user_level:
                return fn()
            else:
                flash("You are not authenticated for this action.")
                return url_for('posts')
        else:
            flash("You are not logged in.")
            return url_for('login')

@app.before_request
def setup_database_connection():
    """
    Creates database objects
    """
    g.db = database.DataBase(app.config['CONNECTION'])

@app.route('/')
@app.route('/posts/')
@app.route('/posts/<int:year>')
@app.route('/posts/<int:year>/<int:month>')
def posts(year=None, month=None):
    """
    Handles display of all posts including front page and archived.
    """
    page = request.args.get('page')
    if page:
        page = int(page) * int(app.config['PER_PAGE'])
    if year or (year and month):
        posts = g.db.get_published_posts(year=year, month=month, page=page)
    else:
        posts = g.db.get_published_posts(page=page)
    return render_template('posts.jinja.html', posts=posts)

@app.route('/posts/<int:year>/<int:month>/<post_name>')
def post(year=None, month=None, post_name=None):
    post = g.db.get_post(year=year, month=month, post_name=post_name)
    render_template('post.jinja.html', post=post)
    
@is_admin
@app.route("/posts/preview")
def preview(methods=['POST']):
    """
    Given a form generate what the post would look like.
    """
    pass

@is_admin
@app.route('/posts/list', methods=["GET"])
def post_list():
    posts = g.db.get_all_posts()
    return render_template("list.jinja.html", posts=posts)

@is_admin
@app.route('/posts/new', methods=["GET", "POST"])
@app.route('/posts/<id_val>/edit', methods=["GET", "POST"])
def change(id_val=None):
    """
    Edit or add a new post
    """
    # populate form with data
    if form.validate_on_submit():
        user = get_user()
        post = database.Post.from_form(form, user)
        g.db.add_post(post)
        if id_val:
            flash("Post has been updated.")
        else:
            flash("Post has been stored.")
        return redirect(url_for("change", id_val=id_val))
    elif request.method == "POST":
        flash("Post could not be saved. Check for validation errors.")
        for error in form.errors:
            flash("%s: %s" % (error, form.errors[error]))
    return render_template("forms.jinja.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if not session.get("username"):
        form = Login()
        if form.validate_on_submit():
            user = g.db.get_user(form.username.data)
            if user and user.password_matches(form.password.data):
                session['username'] = user.username
                flash("Logged in successfully")
                return redirect(url_for("posts"))
            else:
                flash("That username and password combination could not be found.")
        elif request.method == "POST":
            flash("The form is not valid.")
        return render_template('forms.jinja.html', form=form)
    else:
        flash("""You are already logged in.""")
        return redirect(url_for("posts"))
        
@app.route('/logout')
def logout():
    if session.get("username"):
        session.pop("username")
        flash("""You have been logged out.""")
    else:
        flash("You are not logged in.")
    return redirect(url_for("posts"))

@app.route('/config', methods=["GET", "POST"])
def config():
    pass
    

if __name__ == '__main__':
    app.permanent_session_lifetime = timedelta(**app.config['PERMANENT_LOGON_TIMEOUT'])
    app.run()
