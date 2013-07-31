from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app
from models.forms import Login
from time import sleep

accounts = Blueprint("accounts", __name__)

@accounts.route("/login", methods=["GET", "POST"])
@accounts.route("/logon", methods=["GET", "POST"])
def logon():
    account = Login()
    if not session.get('user'):
        if account.validate_on_submit():
            sleep(1) # delay the login process to slow brute force
            user = g.database.engine.get_user(account.data['username'])
            if user and user.password_matches(account.data['password']):
                session['user'] = user.username
                flash("Logged in successfully.")
            else:
                flash("Username or password incorrect.")
    else:
        flash("You are already logged in.")
    return render_template("login.jinja.html", form=account, page_name="Login", content_name="Please Login")
    
@accounts.route("/logout")
def logout():
    if session.get("user"):
        del session['user']
        flash("You have been logged out.")
    else:
        flash("You were not logged in.")
    return redirect(url_for(".logon"))

@accounts.route("/user/<username>")
def user(username):
    # display user details
    pass
