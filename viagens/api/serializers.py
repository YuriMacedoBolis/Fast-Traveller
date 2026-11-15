from datetime import date

from rest_framework import serializers

from viagens.models import AtracaoViagem, Categoria, Viagem


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome", "slug", "custo_medio", "tempo_medio_horas"]


class ViagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viagem
        fields = [
            "id",
            "destino",
            "duracao_dias",
            "orcamento_total",
            "data_inicio",
            "data_criacao",
        ]
        read_only_fields = ["id", "data_criacao"]

    def validate_destino(self, valor):
        limpo = valor.strip()
        if len(limpo) < 3:
            raise serializers.ValidationError("Informe um destino com pelo menos 3 caracteres.")
        return limpo

    def validate_data_inicio(self, valor):
        if valor < date.today():
            raise serializers.ValidationError("A data de início não pode estar no passado.")
        return valor

    def validate_orcamento_total(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("O orçamento deve ser maior que zero.")
        return valor


class AtracaoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = AtracaoViagem
        fields = [
            "id",
            "nome",
            "categoria",
            "custo_estimado",
            "tempo_estimado_horas",
            "endereco",
            "dia",
        ]


class AtracaoCreateSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categoria.objects.all()
    )

    class Meta:
        model = AtracaoViagem
        fields = [
            "id",
            "nome",
            "categoria",
            "custo_estimado",
            "tempo_estimado_horas",
            "endereco",
            "api_external_id",
            "dia",
        ]
        read_only_fields = ["id"]


class AtracoesViagemSerializer(serializers.Serializer):
    viagem_id = serializers.IntegerField()
    destino = serializers.CharField()
    atracoes = AtracaoSerializer(many=True)


class RelatorioSerializer(serializers.Serializer):
    viagem_id = serializers.IntegerField()
    destino = serializers.CharField()
    orcamento_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    custo_total_estimado = serializers.DecimalField(max_digits=10, decimal_places=2)
    saldo_restante = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_atracoes = serializers.IntegerField()
    gastos_por_categoria = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )


class SugestaoSerializer(serializers.Serializer):
    nome = serializers.CharField()
    endereco = serializers.CharField(allow_blank=True)
    categoria = serializers.CharField()
    categoria_nome = serializers.CharField()
    custo_estimado = serializers.DecimalField(max_digits=10, decimal_places=2)
    tempo_estimado_horas = serializers.DecimalField(max_digits=4, decimal_places=2)
    api_external_id = serializers.CharField(allow_blank=True)
    distancia = serializers.IntegerField(allow_null=True)
    cabe_no_orcamento = serializers.BooleanField()


class SugestoesRespostaSerializer(serializers.Serializer):
    fonte = serializers.CharField()
    aviso = serializers.CharField(allow_blank=True)
    sugestoes = SugestaoSerializer(many=True)
