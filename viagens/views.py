from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from viagens.api.serializers import AtracaoSerializer
from viagens.forms import BuscaViagemForm, ViagemForm
from viagens.models import Categoria, Viagem
from viagens.services.sugestoes import calcular_relatorio


class ViagemListView(LoginRequiredMixin, ListView):
    model = Viagem
    template_name = "viagens/lista.html"
    context_object_name = "viagens"

    def get_queryset(self):
        queryset = Viagem.objects.filter(usuario=self.request.user).prefetch_related(
            "atracoes__categoria"
        )

        self.busca = BuscaViagemForm(self.request.GET or None)
        if self.busca.is_valid():
            destino = self.busca.cleaned_data.get("destino")
            if destino:
                queryset = queryset.filter(destino__icontains=destino)

            data_apos = self.busca.cleaned_data.get("data_inicio_apos")
            if data_apos:
                queryset = queryset.filter(data_inicio__gte=data_apos)

            orcamento_min = self.busca.cleaned_data.get("orcamento_min")
            if orcamento_min is not None:
                queryset = queryset.filter(orcamento_total__gte=orcamento_min)

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["busca"] = self.busca
        contexto["tem_filtro"] = any(self.request.GET.get(c) for c in self.busca.fields)
        return contexto


class ViagemDetailView(LoginRequiredMixin, DetailView):
    model = Viagem
    template_name = "viagens/roteiro.html"
    context_object_name = "viagem"

    def get_queryset(self):
        return Viagem.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        categorias = Categoria.objects.all()
        atracoes = self.object.atracoes.select_related("categoria")
        contexto["categorias"] = categorias
        contexto["nomes_categorias"] = {c.slug: c.nome for c in categorias}
        contexto["atracoes"] = AtracaoSerializer(atracoes, many=True).data
        return contexto


class ViagemRelatorioView(LoginRequiredMixin, DetailView):
    model = Viagem
    template_name = "viagens/relatorio.html"
    context_object_name = "viagem"

    def get_queryset(self):
        return Viagem.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        relatorio = calcular_relatorio(self.object)
        custo_total = relatorio["custo_total_estimado"]
        nomes = dict(Categoria.objects.values_list("slug", "nome"))

        gastos = []
        for slug, valor in relatorio["gastos_por_categoria"].items():
            porcentagem = valor / custo_total * 100 if custo_total else 0
            gastos.append({"nome": nomes.get(slug, slug), "valor": valor, "porcentagem": porcentagem})
        gastos.sort(key=lambda gasto: gasto["valor"], reverse=True)

        contexto["relatorio"] = relatorio
        contexto["gastos"] = gastos
        contexto["uso_orcamento"] = relatorio["custo_total_estimado"] / relatorio["orcamento_total"] * 100
        contexto["estouro"] = -relatorio["saldo_restante"]
        return contexto


class ViagemCreateView(LoginRequiredMixin, CreateView):
    model = Viagem
    form_class = ViagemForm
    template_name = "viagens/formulario.html"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Viagem criada! Agora escolha suas atrações.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Confira os campos destacados abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("viagens:roteiro", args=[self.object.pk])


class ViagemUpdateView(LoginRequiredMixin, UpdateView):
    model = Viagem
    form_class = ViagemForm
    template_name = "viagens/formulario.html"

    def get_queryset(self):
        return Viagem.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Viagem atualizada.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Confira os campos destacados abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("viagens:lista")


class ViagemDeleteView(LoginRequiredMixin, DeleteView):
    model = Viagem
    template_name = "viagens/confirmar_exclusao.html"
    success_url = reverse_lazy("viagens:lista")

    def get_queryset(self):
        return Viagem.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Viagem excluída.")
        return super().form_valid(form)
