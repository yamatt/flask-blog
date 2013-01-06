from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app
from models.forms import Post
from decorators import is_admin

posts = Blueprint("posts", __name__)

@posts.route("/<int:year>")
@posts.route("/<int:year>/<int:month>")
def archive(year=None, month=None):
    posts = g.database.engine.get_published_posts(year, month)
    return render_template("posts.jinja.html", posts=posts)
    
@posts.route("/<int:year>/<int:month>/<string:name>")
def show(year, month, name):
    post = g.database.engine.get_published_post(year, month, name)
    if post:
        return render_template("post.jinja.html", item=post)
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
    return render_template("forms.jinja.html", form=form)

@posts.route("/id/<identifier>/edit", methods=["GET", "POST"])
@is_admin
def edit(identifier):
    post = g.database.engine.get_post_by_id(identifier)
    form = Post(obj=post)
    if form.validate_on_submit():
        edited_post = g.database.models.Post.from_form(form, session['user'])
        g.database.engine.add_post(edited_post)
        flash("Saved.")
    return render_template("forms.jinja.html", form=form)


@posts.route("/id/<identifier>/delete", methods=["GET", "POST"])
@is_admin
def delete(identifier):
    pass
    
    

