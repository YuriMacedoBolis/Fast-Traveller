"""Popula a tabela de categorias com os valores padrao do fast Traveller.

O comando e idempotente: pode ser executado a cada deploy sem duplicar dados.
As categorias carregam o mapeamento para a API externa (Geoapify) e a
heuristica de custo/tempo usada para estimar o orcamento do roteiro.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand

from viagens.models import Categoria

# nome, slug, categorias na Geoapify, custo medio (R$), tempo medio (horas)
CATEGORIAS_PADRAO = [
    ("Museu", "museu", "entertainment.museum", "30.00", "2.50"),
    ("Cinema", "cinema", "entertainment.cinema", "35.00", "2.50"),
    ("Gastronomia", "gastronomia", "catering.restaurant", "80.00", "1.50"),
    ("Shopping", "shopping", "commercial.shopping_mall", "150.00", "3.00"),
    ("Parque", "parque", "leisure.park", "0.00", "2.00"),
    (
        "Ponto turístico",
        "turismo",
        "tourism.attraction,tourism.sights",
        "20.00",
        "1.50",
    ),
    (
        "Teatro",
        "teatro",
        "entertainment.culture.theatre,entertainment.culture.arts_centre",
        "90.00",
        "2.50",
    ),
    (
        "Zoológico e aquário",
        "zoologico",
        "entertainment.zoo,entertainment.aquarium",
        "60.00",
        "3.00",
    ),
]


class Command(BaseCommand):
    help = "Cria ou atualiza as categorias padrao de lazer."

    def handle(self, *args, **options):
        criadas = 0
        atualizadas = 0

        for nome, slug, geo, custo, tempo in CATEGORIAS_PADRAO:
            _, criada = Categoria.objects.update_or_create(
                slug=slug,
                defaults={
                    "nome": nome,
                    "geoapify_categories": geo,
                    "custo_medio": Decimal(custo),
                    "tempo_medio_horas": Decimal(tempo),
                },
            )
            if criada:
                criadas += 1
            else:
                atualizadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Categorias: {criadas} criada(s), {atualizadas} atualizada(s)."
            )
        )
