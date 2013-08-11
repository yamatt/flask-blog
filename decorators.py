from functools import wraps
from flask import session, flash, redirect, url_for, g
from enums import AuthorisationLevels

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = g.database.engine.get_user(session['user'])
        if user:
            if user.authorisation_level >= AuthorisationLevels.ADMIN:
                return f(*args, **kwargs)
            else:
                flash("Your account does not allow access to this.")
                return redirect(url_for('posts'))
        else:
            flash("You are not logged in.")
            return redirect(url_for('accounts.logon'))
    return decorated_function
