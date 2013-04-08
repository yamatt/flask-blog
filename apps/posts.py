from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app
from models.forms import Post
from decorators import is_admin

posts = Blueprint("posts", __name__)


@posts.route("/list")
@is_admin
def list():
    posts = g.database.engine.get_all_posts()
    return render_template("post_list.jinja.html", posts=posts, page_name="List of Posts")

@posts.route("/<int:year>")
@posts.route("/<int:year>/<int:month>")
def archive(year=None, month=None):
    posts = g.database.engine.get_published_posts(year, month)
    return render_template("posts.jinja.html", posts=posts, page_name="Posts for {0}/{1}".format(year, month))
    
@posts.route("/<int:year>/<int:month>/<string:name>")
def show(year, month, name):
    post = g.database.engine.get_published_post(year, month, name)
    if post:
        return render_template("post.jinja.html", item=post, page_name=post.title)
    abort(404)
    
@posts.route("/new", methods=["GET", "POST"])
@is_admin
def new():
    form = Post()
    if form.validate_on_submit():
        new_post = g.database.models.Post.from_form(form, session['user'])
        saved_post = g.database.engine.add_post(new_post)
        flash("Saved.")
        return redirect(url_for(".edit", identifier=saved_post.id_val))
    return render_template("forms.jinja.html", form=form, page_name="New post")
    
@posts.route("/id/<identifier>")
@is_admin
def show_from_id(identifier):
    post = g.database.engine.get_post_by_id(identifier)
    if post:
        return render_template("post.jinja.html", item=post, page_name=post.name)
    abort(404)

@posts.route("/id/<identifier>/edit", methods=["GET", "POST"])
@is_admin
def edit(identifier):
    post = g.database.engine.get_post_by_id(identifier)
    form = Post(obj=post)
    if form.validate_on_submit():
        edited_post = g.database.models.Post.from_form(form, session['user'])
        g.database.engine.add_post(edited_post)
        flash("Saved.")
    return render_template("forms.jinja.html", form=form, page_name="Editing post '{0}'".format(post.title))
    
@posts.route("/<int:year>/<int:month>/<string:name>/edit")
@is_admin
def edit_redirect(year, month, name):
    post = g.database.engine.get_published_post(year, month, name)
    if post:
        return redirect(url_for(".edit", identifier=post.id_val))
    abort(404)



@posts.route("/id/<identifier>/delete", methods=["GET", "POST"])
@is_admin
def delete(identifier):
    pass
    
    

