from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app

posts = Blueprint("posts", __name__)

@posts.route("/<int:year>")
@posts.route("/<int:year>/<int:month>")
def archive(year=None, month=None):
    pass
    
@posts.route("/new")
def new():
    return str(current_app.config['PERMANENT_LOGON_TIMEOUT'])

@posts.route("/<int:year>/<int:month>/<string:title>")
def show(year, month, title):
    pass

@posts.route("/<int:year>/<int:month>/<string:title>/edit")
def edit(year, month, title):
    pass

@posts.route("/<int:year>/<int:month>/<string:title>/delete")
def delete(year, month, title):
    pass
