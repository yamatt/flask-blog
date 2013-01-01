from datetime import timedelta

DEBUG=True

#Blog
TITLE="Template Blog"
SUBTITLE="An awesome blog."
SECRET_KEY = """CHANGE ME!!!"""
ADMIN_USERNAME = "admin"
PER_PAGE=15
PERMANENT_SESSION_LIFETIME = timedelta(days=365)
TIME_LOCALE="Europe/London"
PARSER="Markdown"

#Database
DATABASE_ENGINE="sqlite"
DATABASE_CONNECTION_STRING="blog.db"

