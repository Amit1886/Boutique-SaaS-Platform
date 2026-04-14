import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _env_list(name: str, default: list[str]) -> list[str]:
    value = (os.environ.get(name) or "").strip()
    if not value:
        return default
    # Comma-separated values (optionally with semicolons).
    parts = []
    for part in value.replace(";", ",").split(","):
        cleaned = part.strip()
        if cleaned:
            parts.append(cleaned)
    return parts or default


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS: list[str] = _env_list("DJANGO_ALLOWED_HOSTS", ["localhost", "127.0.0.1", "[::1]"])
CSRF_TRUSTED_ORIGINS: list[str] = _env_list("DJANGO_CSRF_TRUSTED_ORIGINS", [])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "accounts.apps.AccountsConfig",
    "vendors.apps.VendorsConfig",
    "boutique.apps.BoutiqueConfig",
    "tryon_ai.apps.TryonAiConfig",
    "orders.apps.OrdersConfig",
    "tailors.apps.TailorsConfig",
    "inventory.apps.InventoryConfig",
    "pos.apps.PosConfig",
    "payments.apps.PaymentsConfig",
    "analytics.apps.AnalyticsConfig",
    "api.apps.ApiConfig",
    "mobile_api.apps.MobileApiConfig",
    "deployhook.apps.DeployhookConfig",
    "whatsapp_bot.apps.WhatsappBotConfig",
    "wallet.apps.WalletConfig",
    "magic_studio.apps.MagicStudioConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "accounts.middleware.ProfileLanguageMiddleware",
    "vendors.middleware.VendorRoutingMiddleware",
]

ROOT_URLCONF = "boutique_ai_saas.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "vendors.context_processors.vendor_context",
                "accounts.context_processors.user_context",
            ],
        },
    }
]

WSGI_APPLICATION = "boutique_ai_saas.wsgi.application"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("hi", "Hindi"),
    ("ta", "Tamil"),
    ("gu", "Gujarati"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}

VENDOR_PATH_PREFIX_ENABLED = True
MAIN_DOMAIN = os.environ.get("MAIN_DOMAIN", "localhost")

# External integrations (optional)
HF_API_TOKEN = os.environ.get("HF_API_TOKEN", "")
HF_RMBG_MODEL = os.environ.get("HF_RMBG_MODEL", "facebook/mask2former-swin-large-coco-panoptic")
HF_TRYON_MODEL = os.environ.get("HF_TRYON_MODEL", "")
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")

DEFAULT_UPI_ID = os.environ.get("DEFAULT_UPI_ID", "")
WALLET_CASHBACK_RATE = os.environ.get("WALLET_CASHBACK_RATE", "0.02")  # 2%
WALLET_REFERRAL_BONUS = os.environ.get("WALLET_REFERRAL_BONUS", "25.00")  # INR

# Magic Studio (React SPA + token-protected admin API)
MAGIC_ADMIN_TOKEN = os.environ.get("MAGIC_ADMIN_TOKEN", os.environ.get("ADMIN_TOKEN", "change-me"))

# Production hardening (safe defaults; tune via env vars)
if not DEBUG:
    # PythonAnywhere and most reverse proxies set X-Forwarded-Proto.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "1") == "1"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
