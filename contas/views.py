from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from contas.forms import CadastroForm


class CadastroView(CreateView):
    form_class = CadastroForm
    template_name = "contas/cadastro.html"
    success_url = reverse_lazy("viagens:lista")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.shortcuts import redirect

            return redirect("viagens:lista")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        resposta = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Conta criada! Bem-vindo ao fast Traveller.")
        return resposta

    def form_invalid(self, form):
        messages.error(self.request, "Confira os campos destacados abaixo.")
        return super().form_invalid(form)


class EntrarView(LoginView):
    template_name = "contas/login.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha incorretos.")
        return super().form_invalid(form)


class SairView(LogoutView):
    next_page = reverse_lazy("home")
