from flask import Flask
from apps.posts import posts
import settings
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(settings)

app.register_blueprint(posts, url_prefix="/posts")

if __name__ == "__main__":
    app.permanent_session_lifetime = timedelta(**app.config['PERMANENT_LOGON_TIMEOUT'])
    app.run()
