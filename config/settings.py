from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
import cloudinary

cloudinary.config(
    secure=True,
)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv(
    "DEBUG",
    "True",
).lower() == "true"


ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]


CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "",
    ).split(",")
    if origin.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary",
    "users_app",
    "pets_app",
    "health_app",
    "lostfound_app",
    "community_app",
    "adoption_app",
    "vets_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.locale.LocaleMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "health_app.context_processors.firebase_public_settings",
            ],
        },
    },
]

# ============================================================
# DATABASE
# Local development:
#     normal local MySQL
#
# Production on Render:
#     TiDB Cloud over TLS
# ============================================================

DB_OPTIONS = {
    "charset": "utf8mb4",
}


# Enable secure TLS connection only when DB_SSL_CA
# is supplied by the production environment.
if os.getenv("DB_SSL_CA"):

    DB_OPTIONS.update({

        "ssl_ca": os.getenv(
            "DB_SSL_CA"
        ),

        "ssl_verify_cert": True,

        "ssl_verify_identity": True,

    })


DATABASES = {

    "default": {

        "ENGINE":
            "django.db.backends.mysql",

        "NAME":
            os.getenv("DB_NAME"),

        "USER":
            os.getenv("DB_USER"),

        "PASSWORD":
            os.getenv("DB_PASSWORD"),

        "HOST":
            os.getenv(
                "DB_HOST",
                "localhost",
            ),

        "PORT":
            os.getenv(
                "DB_PORT",
                "3306",
            ),

        "OPTIONS":
            DB_OPTIONS,
    }

}

AUTH_PASSWORD_VALIDATORS = []
AUTH_USER_MODEL = "users_app.User"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


STORAGES = {
    "default": {
        "BACKEND":
            "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND":
            "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# PRIMARY KEYS
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# PRODUCTION PROXY / HTTPS
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"

from django.utils.translation import gettext_lazy as _


LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("bn", _("বাংলা")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# ============================================================
# FIREBASE CLOUD MESSAGING
# ============================================================

FIREBASE_API_KEY = os.getenv(
    "FIREBASE_API_KEY",
    ""
)

FIREBASE_AUTH_DOMAIN = os.getenv(
    "FIREBASE_AUTH_DOMAIN",
    ""
)

FIREBASE_PROJECT_ID = os.getenv(
    "FIREBASE_PROJECT_ID",
    ""
)

FIREBASE_STORAGE_BUCKET = os.getenv(
    "FIREBASE_STORAGE_BUCKET",
    ""
)

FIREBASE_MESSAGING_SENDER_ID = os.getenv(
    "FIREBASE_MESSAGING_SENDER_ID",
    ""
)

FIREBASE_APP_ID = os.getenv(
    "FIREBASE_APP_ID",
    ""
)

FIREBASE_VAPID_KEY = os.getenv(
    "FIREBASE_VAPID_KEY",
    ""
)

FIREBASE_SERVICE_ACCOUNT_FILE = (
    BASE_DIR / "firebase-service-account.json"
)

# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD",
    ""
)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER