from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app

frontpage = Blueprint("frontpage", __name__)

@frontpage.route("/")
def show():
    posts = g.database.engine.get_published_posts()
    return render_template("posts.jinja.html", posts=posts)
    
