from django.urls import path

from contas.views import CadastroView, EntrarView, SairView

urlpatterns = [
    path("login/", EntrarView.as_view(), name="login"),
    path("logout/", SairView.as_view(), name="logout"),
    path("cadastro/", CadastroView.as_view(), name="cadastro"),
]
