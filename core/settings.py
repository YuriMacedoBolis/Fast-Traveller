"""Configuracoes do projeto fast Traveller.

Todas as configuracoes sensiveis sao lidas de variaveis de ambiente. Em
desenvolvimento, elas podem vir de um arquivo .env (nunca versionado).
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def env_list(nome, padrao=""):
    """Le uma variavel de ambiente separada por virgulas e devolve uma lista."""
    bruto = os.environ.get(nome, padrao)
    return [item.strip() for item in bruto.split(",") if item.strip()]


# ---------------------------------------------------------------------------
# Nucleo
# ---------------------------------------------------------------------------
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# Em producao a chave e obrigatoria. Em desenvolvimento geramos uma efemera
# para que o projeto rode logo apos o clone, sem segredo algum no repositorio.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        from django.core.management.utils import get_random_secret_key

        SECRET_KEY = get_random_secret_key()
    else:
        raise RuntimeError(
            "DJANGO_SECRET_KEY nao definida. Configure a variavel de ambiente "
            "antes de executar em producao."
        )

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")

host_render = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if host_render:
    ALLOWED_HOSTS.append(host_render)

if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1", "testserver"]

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceiros
    "rest_framework",
    "drf_spectacular",
    # Aplicacoes do projeto
    "contas",
    "viagens",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

AUTH_USER_MODEL = "contas.Usuario"


# ---------------------------------------------------------------------------
# Banco de dados
# ---------------------------------------------------------------------------
# Em producao usamos o pooler do Supabase em session mode (porta 5432).
# A conexao direta do Supabase e IPv6-only e o Render nao tem IPv6 de saida.
SQLITE_PADRAO = "sqlite:///" + str(BASE_DIR / "db.sqlite3")

# Uma DATABASE_URL definida porem vazia (comum em .env preenchido pela metade)
# deve cair no SQLite de desenvolvimento, e nao quebrar a configuracao.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip() or SQLITE_PADRAO

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=60,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# Internacionalizacao
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Arquivos estaticos (bloco da trilha de frontend/deploy)
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------------------
# Autenticacao (web)
# ---------------------------------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/viagens/"
LOGOUT_REDIRECT_URL = "/login/"


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
# DatabaseCache e compartilhado entre os workers do gunicorn e sobrevive ao
# spin-down do plano free do Render, ao contrario do LocMemCache.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_geoapify",
        "TIMEOUT": 60 * 60 * 24,
        "OPTIONS": {"MAX_ENTRIES": 2000},
    }
}


# ---------------------------------------------------------------------------
# API externa - Geoapify (bloco da trilha de backend)
# ---------------------------------------------------------------------------
GEOAPIFY_API_KEY = os.environ.get("GEOAPIFY_API_KEY", "")
GEOAPIFY_TIMEOUT = float(os.environ.get("GEOAPIFY_TIMEOUT", "5"))
GEOAPIFY_CACHE_TTL = int(os.environ.get("GEOAPIFY_CACHE_TTL", 60 * 60 * 24))
GEOAPIFY_RAIO_PADRAO_M = int(os.environ.get("GEOAPIFY_RAIO_PADRAO_M", "5000"))


# ---------------------------------------------------------------------------
# Django REST Framework (bloco da trilha de backend)
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "120/hour",
        "sugestoes": "30/hour",
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "fast Traveller API",
    "DESCRIPTION": (
        "API REST do fast Traveller: planejamento de roteiros de viagem com "
        "controle de orcamento. UniCEUB - Desenvolvimento Web."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}


# ---------------------------------------------------------------------------
# Seguranca em producao (bloco da trilha de frontend/deploy)
# ---------------------------------------------------------------------------
if not DEBUG:
    # O Render termina o TLS no proxy; sem isso o Django nao reconhece HTTPS.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simples": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simples"}
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
