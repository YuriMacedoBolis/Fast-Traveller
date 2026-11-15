from django.contrib import admin

from .models import AtracaoViagem, Categoria, Viagem


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug", "custo_medio", "tempo_medio_horas")
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome", "slug")


class AtracaoViagemInline(admin.TabularInline):
    model = AtracaoViagem
    extra = 0
    autocomplete_fields = ("categoria",)


@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = (
        "destino",
        "usuario",
        "data_inicio",
        "duracao_dias",
        "orcamento_total",
        "data_criacao",
    )
    list_filter = ("data_inicio", "data_criacao")
    search_fields = ("destino", "usuario__username", "usuario__email")
    date_hierarchy = "data_inicio"
    inlines = [AtracaoViagemInline]


@admin.register(AtracaoViagem)
class AtracaoViagemAdmin(admin.ModelAdmin):
    list_display = ("nome", "viagem", "categoria", "custo_estimado", "dia")
    list_filter = ("categoria",)
    search_fields = ("nome", "endereco", "viagem__destino")
