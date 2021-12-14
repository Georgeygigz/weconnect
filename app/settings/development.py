from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

VERIFY_URL = os.getenv("VERIFY_URL", "")
