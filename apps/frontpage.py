from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app

frontpage = Blueprint("frtonpage", __name__)

@frontpage.route("/")
def archive():
    posts = g.database.engine.get_published_posts()
    return render_template("posts.jinja.html", posts=posts)
	
