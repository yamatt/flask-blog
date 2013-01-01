from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app
from models.forms import Post

posts = Blueprint("posts", __name__)

@posts.route("/<int:year>")
@posts.route("/<int:year>/<int:month>")
def archive(year=None, month=None):
    pass
    
@posts.route("/new", methods=["GET", "POST"])
def new():
    post = Post()
    if post.validate_on_submit():
        new_post = g.database.Post.from_form(post)
    return render_template("forms.jinja.html", form=post)
    
    
@posts.route("/<int:year>/<int:month>/<string:title>")
def show(year, month, title):
    pass

@posts.route("/<int:year>/<int:month>/<string:title>/edit")
def edit(year, month, title):
    pass

@posts.route("/<int:year>/<int:month>/<string:title>/delete")
def delete(year, month, title):
    pass
