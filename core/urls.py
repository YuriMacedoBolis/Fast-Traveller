from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core.views import HomeView, healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("viagens.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("healthz/", healthz, name="healthz"),
    path("", include("contas.urls")),
    path("", include("viagens.urls")),
    path("", HomeView.as_view(), name="home"),
]
