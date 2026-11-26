from django.urls import path

from viagens.views import (
    ViagemCreateView,
    ViagemDeleteView,
    ViagemDetailView,
    ViagemListView,
    ViagemUpdateView,
)

app_name = "viagens"

urlpatterns = [
    path("viagens/", ViagemListView.as_view(), name="lista"),
    path("viagens/nova/", ViagemCreateView.as_view(), name="nova"),
    path("viagens/<int:pk>/", ViagemDetailView.as_view(), name="roteiro"),
    path("viagens/<int:pk>/editar/", ViagemUpdateView.as_view(), name="editar"),
    path("viagens/<int:pk>/excluir/", ViagemDeleteView.as_view(), name="excluir"),
]
