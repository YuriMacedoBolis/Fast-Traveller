"""Views de nivel de projeto: pagina inicial e health check."""

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Pagina inicial publica.

    Usuarios autenticados sao levados direto para a lista de viagens.
    """

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/viagens/")
        return super().get(request, *args, **kwargs)


def healthz(request):
    """Endpoint leve usado pelo health check do Render.

    Nao toca o banco de proposito: serve apenas para dizer que o processo
    esta de pe e respondendo.
    """
    return JsonResponse({"status": "ok"})
