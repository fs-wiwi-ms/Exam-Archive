import os

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

# TODO: Define allowed hosts
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# TODO: Define database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "./db.sqlite3",
    }
}
