from __future__ import annotations

from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).parent

DEBUG = True

SECRET_KEY = "django-insecure-6-@0$ah01nfjv0+6f-9%eq2oqngwm#qtxy-ntpj+7hpz-*+q^("

# Dangerous: disable host header validation
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "example",
    "reporting_endpoints",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.admin",
]

MIDDLEWARE = [
    "django.middleware.csrf.CsrfViewMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "reporting_endpoints.middleware.ReportingEndpointsMiddleware",
]

ROOT_URLCONF = "example.urls"

DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "example.sqlite3",
    }
}

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
            ]
        },
    }
]

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

CSP_DEFAULT_SRC = "'self'"
CSP_REPORT_URI = "/_/csp-reports/"
CSP_REPORT_TO = "csp-violations"
CSP_REPORT_ONLY = False

REPORTING_ENDPOINTS = {"csp-violations": "/_/csp-reports/"}
REPORT_TO_ENDPOINTS = [
    {
        "group": "csp-violations",
        "max_age": 10886400,
        "endpoints": [{"url": "/_/csp-reports/"}],
    }
]
