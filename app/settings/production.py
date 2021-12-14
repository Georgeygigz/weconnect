from .base import *
import dj_database_url

if os.getenv("DJANGO_ENV", ""):
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES["default"].update(db_from_env)


DEBUG = False

ALLOWED_HOSTS = ["*"]

VERIFY_URL = os.getenv("VERIFY_URL", "")
