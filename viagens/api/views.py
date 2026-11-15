from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from viagens.api.filters import aplicar_filtros
from viagens.api.permissions import IsOwner
from viagens.api.serializers import (
    AtracaoCreateSerializer,
    AtracaoSerializer,
    AtracoesViagemSerializer,
    CategoriaSerializer,
    RelatorioSerializer,
    SugestoesRespostaSerializer,
    ViagemSerializer,
)
from viagens.models import Categoria, Viagem
from viagens.services.geoapify import DestinoNaoEncontrado
from viagens.services.sugestoes import calcular_relatorio, obter_sugestoes

PARAMETROS_BUSCA = [
    OpenApiParameter("destino", str, description="Busca parcial pelo destino."),
    OpenApiParameter("orcamento_min", str, description="Orçamento mínimo."),
    OpenApiParameter("orcamento_max", str, description="Orçamento máximo."),
    OpenApiParameter("data_inicio_apos", str, description="Data inicial (AAAA-MM-DD)."),
    OpenApiParameter("data_inicio_antes", str, description="Data final (AAAA-MM-DD)."),
    OpenApiParameter("duracao_min", int, description="Duração mínima em dias."),
    OpenApiParameter("duracao_max", int, description="Duração máxima em dias."),
]


class CategoriaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()
    pagination_class = None


@extend_schema(tags=["viagens"])
class ViagemViewSet(viewsets.ModelViewSet):
    serializer_class = ViagemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = None
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["data_inicio", "orcamento_total", "data_criacao", "destino"]
    ordering = ["-data_criacao"]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Viagem.objects.none()
        queryset = Viagem.objects.filter(usuario=self.request.user).prefetch_related(
            "atracoes__categoria"
        )
        return aplicar_filtros(queryset, self.request.query_params)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @extend_schema(parameters=PARAMETROS_BUSCA)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(responses=AtracoesViagemSerializer)
    @action(detail=True, methods=["get"], url_path="atracoes")
    def atracoes(self, request, pk=None):
        viagem = self.get_object()
        dados = {
            "viagem_id": viagem.pk,
            "destino": viagem.destino,
            "atracoes": viagem.atracoes.select_related("categoria"),
        }
        return Response(AtracoesViagemSerializer(dados).data)

    @extend_schema(request=AtracaoCreateSerializer, responses=AtracaoSerializer)
    @atracoes.mapping.post
    def adicionar_atracao(self, request, pk=None):
        viagem = self.get_object()
        serializer = AtracaoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        atracao = serializer.save(viagem=viagem)
        return Response(AtracaoSerializer(atracao).data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=None)
    @action(
        detail=True,
        methods=["delete"],
        url_path="atracoes/(?P<atracao_id>[0-9]+)",
    )
    def remover_atracao(self, request, pk=None, atracao_id=None):
        viagem = self.get_object()
        atracao = viagem.atracoes.filter(pk=atracao_id).first()
        if atracao is None:
            return Response(
                {"detail": "Atração não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
        atracao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses=RelatorioSerializer)
    @action(detail=True, methods=["get"], url_path="relatorio")
    def relatorio(self, request, pk=None):
        viagem = self.get_object()
        return Response(RelatorioSerializer(calcular_relatorio(viagem)).data)

    @extend_schema(
        responses=SugestoesRespostaSerializer,
        parameters=[
            OpenApiParameter("categorias", str, description="Slugs separados por vírgula."),
            OpenApiParameter("raio", int, description="Raio da busca em metros."),
        ],
    )
    @action(detail=True, methods=["get"], url_path="sugestoes")
    def sugestoes(self, request, pk=None):
        viagem = self.get_object()

        slugs = [s for s in (request.query_params.get("categorias") or "").split(",") if s]

        raio = request.query_params.get("raio")
        try:
            raio = int(raio) if raio else None
        except ValueError:
            return Response(
                {"detail": "O raio deve ser um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            dados = obter_sugestoes(viagem, slugs=slugs, raio_m=raio)
        except DestinoNaoEncontrado as erro:
            return Response({"detail": str(erro)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(SugestoesRespostaSerializer(dados).data)

    sugestoes.throttle_scope = "sugestoes"
