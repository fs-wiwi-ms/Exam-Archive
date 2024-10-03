import importlib
from pathlib import Path

# Common settings
BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "rest_framework",
    "core.apps.CoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "examarchive.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "examarchive.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"
# LANGUAGE_CODE = "de-DE"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Custom Settings
EXAM_MIN_YEAR = 2000
EXAM_MAX_YEAR = 2050
SEMESTER_SETTINGS = [
    {
        "code": "WS",
        "display_name": "Winter Semester",
        "start_date": (10, 1),
        "end_date": (3, 31),
    },
    {
        "code": "SS",
        "display_name": "Summer Semester",
        "start_date": (4, 1),
        "end_date": (9, 30),
    },
    {
        "code": "T1",
        "display_name": "Trimester 1",
        "start_date": (1, 1),
        "end_date": (4, 30),
    },
    {
        "code": "T2",
        "display_name": "Trimester 2",
        "start_date": (5, 1),
        "end_date": (8, 31),
    },
    {
        "code": "T3",
        "display_name": "Trimester 3",
        "start_date": (9, 1),
        "end_date": (12, 31),
    },
]
FILE_UPLOAD_ALLOWED_FORMATS = [
    {
        "extension": ".pdf",
        "mime_type": "application/pdf",
        "display_name": "PDF Document",
        "max_size": 10485760,
    },
    {
        "extension": ".doc",
        "mime_type": "application/msword",
        "display_name": "Word Document",
        "max_size": 10485760,
    },
    {
        "extension": ".docx",
        "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "display_name": "DOCX Document",
        "max_size": 10485760,
    },
    {
        "extension": ".png",
        "mime_type": "image/png",
        "display_name": "PNG Image",
        "max_size": 10485760,
    },
]
EXAM_METADATA_AUTHOR = "Unknown Author"


# Define which settings can be overridden by tenants
OVERRIDABLE_SETTINGS = [
    "EXAM_MIN_YEAR",
    "EXAM_MAX_YEAR",
    "SEMESTER_SETTINGS",
    "FILE_UPLOAD_ALLOWED_FORMATS",
    "EXAM_METADATA_AUTHOR",
]


def override_settings():
    """Override settings from the tenant's settings file."""
    try:
        tenant_settings = importlib.import_module("settings")
    except ImportError:
        return

    for setting in OVERRIDABLE_SETTINGS:
        if hasattr(tenant_settings, setting):
            value = getattr(tenant_settings, setting)
            globals()[setting] = value


override_settings()
