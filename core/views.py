from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/viagens/")
        return super().get(request, *args, **kwargs)


def healthz(request):
    return JsonResponse({"status": "ok"})
