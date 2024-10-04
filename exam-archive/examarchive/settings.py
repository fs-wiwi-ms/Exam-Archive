import os
from pathlib import Path

from dotenv import load_dotenv

# Load the .env file
load_dotenv("./.env")
load_dotenv("./settings.conf")


def __get_int(key: str, default: int) -> int:
    return int(os.getenv(key, default))


def __get_bool(key: str, default: bool = False) -> bool:
    return bool(os.getenv(key, default))


def __get_list(key: str, default: list[str] | None = None) -> list[str]:
    value = os.getenv(key)
    if value is not None:
        return [item.strip() for item in value.split(",") if item.strip()]
    if default is not None:
        return default
    return []


BASE_DIR: str = Path(__file__).resolve().parent.parent
DEVELOPMENT_ENVIRONMENTS: list[str] = ["dev", "develop", "development"]

DEBUG: bool = False
if os.environ.get("EXAMARCHIVE_ENVIORMENT", "production") in DEVELOPMENT_ENVIRONMENTS:
    DEBUG = True


def _get_secret_key() -> str:
    if "EXAMARCHIVE_SECRET_KEY" in os.environ:
        return os.getenv("EXAMARCHIVE_SECRET_KEY")
    elif DEBUG is True:
        return "development-secret-key-7K#4xCYz8utd4Y5LezEiSjylQs6uH6"
    raise RuntimeError(
        "EXAMARCHIVE_SECRET_KEY is not set in the environment and DEBUG is False. Cannot start the application."
    )


SECRET_KEY: str = _get_secret_key()


def _get_allowed_hosts() -> str:
    if "EXAMARCHIVE_ALLOWED_HOSTS" in os.environ:
        return __get_list("EXAMARCHIVE_ALLOWED_HOSTS")
    elif DEBUG is True:
        return ["127.0.0.1", "localhost"]
    raise RuntimeError(
        "EXAMARCHIVE_ALLOWED_HOSTS is not set in the environment and DEBUG is False. Cannot start the application."
    )


ALLOWED_HOSTS: list[str] = _get_allowed_hosts()

DATABASES: dict[str, dict] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "./db.sqlite3",
    }
}


INSTALLED_APPS: list[str] = [
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
if DEBUG is True:
    AUTH_PASSWORD_VALIDATORS = []


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
DEFAULT_EXAM_MIN_YEAR: int = 2000
EXAM_MIN_YEAR: str = __get_int("EXAMARCHIVE_EXAM_MIN_YEAR", DEFAULT_EXAM_MIN_YEAR)
DEFAULT_EXAM_MAX_YEAR: int = 2050
EXAM_MAX_YEAR: str = __get_int("EXAMARCHIVE_EXAM_MAX_YEAR", DEFAULT_EXAM_MAX_YEAR)

DEFAULT_ACTIVE_PERIODS: str = "semester"
SEMESTER_PERIODS: list[dict] = [
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
]
TRIMESTER_PERIODS: list[dict] = [
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


def _get_academic_periods() -> list[dict]:
    term_structure: str = os.environ.get(
        "EXAMARCHIVE_TERM_STRUCTURE", DEFAULT_ACTIVE_PERIODS
    ).lower()
    if term_structure == "trimester":
        return TRIMESTER_PERIODS
    return SEMESTER_PERIODS


TERMS: list[dict] = _get_academic_periods()


# Internally supported file formats for the Exam model
DEFAULT_EXAM_FILE_FORMATS: list[dict[str, str]] = [
    {
        "extension": ".pdf",
        "mime_type": "application/pdf",
        "display_name": "PDF Document",
    },
    {
        "extension": ".docx",
        "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "display_name": "Word Document",
    },
]


def _get_exam_file_formats() -> list[dict[str, str]]:
    allowed_formats: list[str] | None = __get_list(
        "EXAMARCHIVE_EXAM_ALLOWED_FILE_FORMATS"
    )
    excluded_formats: list[str] | None = __get_list(
        "EXAMARCHIVE_EXAM_EXCLUDED_FILE_FORMATS"
    )
    filtered_formats: list[dict[str, str]] = DEFAULT_EXAM_FILE_FORMATS

    if allowed_formats:
        filtered_formats = [
            fmt for fmt in filtered_formats if fmt["extension"] in allowed_formats
        ]

    if excluded_formats:
        filtered_formats = [
            fmt for fmt in filtered_formats if fmt["extension"] not in excluded_formats
        ]

    return filtered_formats


EXAM_FILE_FORMATS = _get_exam_file_formats()

DEFAULT_EXAM_MAX_UPLOAD_FILE_SIZE: int = 10485760  # 10 MB
EXAM_MAX_UPLOAD_FILE_SIZE: int = __get_int(
    "EXAMARCHIVE_EXAM_MAX_UPLOAD_FILE_SIZE", DEFAULT_EXAM_MAX_UPLOAD_FILE_SIZE
)


DEFAULT_EXAM_METADATA_AUTHOR: str = "Unknown Author"
EXAM_METADATA_AUTHOR: str = os.getenv(
    "EXAMARCHIVE_EXAM_METADATA_AUTHOR", DEFAULT_EXAM_METADATA_AUTHOR
)
