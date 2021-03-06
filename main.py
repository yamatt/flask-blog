#!/usr/bin/env python
# flask
from flask import Flask, g, session, url_for

# config
import settings
from models.interface import DatabaseInterface

# apps
from apps.posts import posts
from apps.accounts import accounts
from apps.frontpage import frontpage
from apps.pages import pages
from apps.upload import upload

# common
from datetime import timedelta, datetime
from pytz import timezone as load_timezone

app = Flask(__name__)
app.config.from_object(settings)

database = DatabaseInterface(settings.DATABASE_ENGINE, settings.DATABASE_CONNECTION_STRING)

@app.template_filter('formatdatetime')
def format_datetime_filter(dt, format="%Y-%m-%d %H:%M %Z"):
    timezone = load_timezone(app.config['TIME_LOCALE'])
    dt = timezone.fromutc(dt)
    return dt.strftime(format)

@app.template_filter('agedatetime')
def format_datetime_filter(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default
    
@app.template_filter("parse")
def set_parser(s):
    parser_name = ".".join(["parsers", settings.PARSER])
    parser_module = __import__(parser_name, globals(), locals(), [settings.PARSER])
    parser = getattr(parser_module, "parser")
    return parser(s)
    
@app.context_processor
def get_page():
    def get_page(name, published=True):
        page = g.database.engine.get_page(name)
        if page and published and page.published:
            return page
    return {"get_page": get_page}
    
@app.context_processor
def latest_posts():
    posts = g.database.engine.get_published_posts()
    return {"latest_posts": posts}
    
@app.context_processor
def add_user():
    user = g.database.engine.get_user(session.get('user'))
    return {"user": user}

@app.before_request
def setup_database():
    g.database = DatabaseInterface(settings.DATABASE_ENGINE, settings.DATABASE_CONNECTION_STRING)

app.url_map.strict_slashes = False

app.register_blueprint(frontpage)
app.register_blueprint(pages)
app.register_blueprint(posts, url_prefix="/posts")
app.register_blueprint(accounts, url_prefix="/accounts")
app.register_blueprint(upload, url_prefix="/upload")

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    

    
if __name__ == "__main__":
    app.run()
