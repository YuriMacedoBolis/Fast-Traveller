"""Rotas raiz do fast Traveller.

Organizacao:
  /                 -> paginas da aplicacao (MTV)
  /api/v1/          -> API REST propria (DRF)
  /api/docs/        -> documentacao navegavel (Swagger UI)
  /api/redoc/       -> documentacao alternativa (Redoc)
  /api/schema/      -> schema OpenAPI 3 em YAML
  /admin/           -> administracao do Django
"""

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core.views import HomeView, healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    # Documentacao da API propria
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Health check usado pelo Render
    path("healthz/", healthz, name="healthz"),
    # Pagina inicial
    path("", HomeView.as_view(), name="home"),
]
