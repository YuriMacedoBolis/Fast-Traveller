from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q, Sum


class Categoria(models.Model):
    nome = models.CharField("nome", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=100, unique=True)
    geoapify_categories = models.CharField(
        "categorias na Geoapify", max_length=255, blank=True
    )
    custo_medio = models.DecimalField(
        "custo medio (R$)",
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    tempo_medio_horas = models.DecimalField(
        "tempo medio (horas)",
        max_digits=4,
        decimal_places=2,
        default=Decimal("1.00"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    class Meta:
        db_table = "categorias"
        ordering = ["nome"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome

    @property
    def lista_geoapify(self):
        return [c.strip() for c in self.geoapify_categories.split(",") if c.strip()]


class Viagem(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="viagens",
        db_column="usuario_id",
        verbose_name="usuário",
    )
    destino = models.CharField("destino", max_length=200)
    duracao_dias = models.PositiveIntegerField(
        "duração (dias)", validators=[MinValueValidator(1), MaxValueValidator(60)]
    )
    orcamento_total = models.DecimalField(
        "orçamento total (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
            MaxValueValidator(Decimal("99999999.99")),
        ],
    )
    data_inicio = models.DateField("data de início")
    data_criacao = models.DateTimeField("data de criação", auto_now_add=True)
    destino_lat = models.FloatField("latitude", null=True, blank=True)
    destino_lon = models.FloatField("longitude", null=True, blank=True)

    class Meta:
        db_table = "viagens"
        ordering = ["-data_criacao"]
        verbose_name = "viagem"
        verbose_name_plural = "viagens"
        indexes = [models.Index(fields=["usuario", "-data_criacao"])]

    def __str__(self):
        return f"{self.destino} ({self.data_inicio:%d/%m/%Y})"

    def clean(self):
        if self.data_inicio and self.data_inicio < date.today():
            raise ValidationError(
                {"data_inicio": "A data de início não pode estar no passado."}
            )

    @property
    def custo_total_estimado(self):
        total = self.atracoes.aggregate(total=Sum("custo_estimado"))["total"]
        return total or Decimal("0.00")

    @property
    def saldo_restante(self):
        return self.orcamento_total - self.custo_total_estimado

    @property
    def tempo_total_estimado(self):
        total = self.atracoes.aggregate(total=Sum("tempo_estimado_horas"))["total"]
        return total or Decimal("0.00")


class AtracaoViagem(models.Model):
    viagem = models.ForeignKey(
        Viagem,
        on_delete=models.CASCADE,
        related_name="atracoes",
        db_column="viagem_id",
        verbose_name="viagem",
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="atracoes",
        db_column="categoria_id",
        verbose_name="categoria",
    )
    nome = models.CharField("nome", max_length=255)
    custo_estimado = models.DecimalField(
        "custo estimado (R$)",
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    tempo_estimado_horas = models.DecimalField(
        "tempo estimado (horas)",
        max_digits=4,
        decimal_places=2,
        default=Decimal("1.00"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    endereco = models.CharField("endereço", max_length=255, blank=True)
    api_external_id = models.CharField(
        "id na API externa", max_length=255, blank=True, db_index=True
    )
    dia = models.PositiveSmallIntegerField("dia do roteiro", null=True, blank=True)

    class Meta:
        db_table = "atracao_viagem"
        ordering = ["dia", "id"]
        verbose_name = "atração da viagem"
        verbose_name_plural = "atrações da viagem"
        constraints = [
            models.UniqueConstraint(
                fields=["viagem", "api_external_id"],
                condition=~Q(api_external_id=""),
                name="uniq_atracao_externa_por_viagem",
            )
        ]

    def __str__(self):
        return self.nome
