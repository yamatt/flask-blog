#!/usr/bin/env python
from flask import Flask, g
from apps.posts import posts
import settings
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(settings)

app.register_blueprint(posts, url_prefix="/posts")

@app.before_request
def setup_database():
    database_name = ".".join(["models", settings.DATABASE_ENGINE])
    database_module = __import__(database_name, globals(), locals(), [])
    g.database = getattr(database_module, settings.DATABASE_ENGINE)
    
@app.before_request
def get_user():
    username = session.get('username')
    if username:
        user = g.database.get_user(username)
        return user
    
if __name__ == "__main__":
    app.run()
