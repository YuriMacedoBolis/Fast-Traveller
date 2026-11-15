from decimal import Decimal

from viagens.models import AtracaoViagem, Categoria
from viagens.services.geoapify import (
    ErroServicoExterno,
    buscar_lugares,
    geocodificar,
)


def _categoria_por_lugar(lugar, categorias):
    tipos = lugar.get("categorias") or []
    melhor = None
    melhor_tamanho = -1

    for categoria in categorias:
        for prefixo in categoria.lista_geoapify:
            for tipo in tipos:
                if tipo == prefixo or tipo.startswith(prefixo + "."):
                    if len(prefixo) > melhor_tamanho:
                        melhor = categoria
                        melhor_tamanho = len(prefixo)

    return melhor


def _montar_sugestao(lugar, categoria, saldo):
    custo = categoria.custo_medio
    tempo = categoria.tempo_medio_horas
    return {
        "nome": lugar["nome"],
        "endereco": lugar["endereco"],
        "categoria": categoria.slug,
        "categoria_nome": categoria.nome,
        "custo_estimado": custo,
        "tempo_estimado_horas": tempo,
        "api_external_id": lugar["api_external_id"],
        "distancia": lugar.get("distancia"),
        "cabe_no_orcamento": custo <= saldo,
    }


def _sugestoes_locais(viagem, categorias):
    base = (
        AtracaoViagem.objects.filter(viagem__destino__iexact=viagem.destino)
        .exclude(viagem_id=viagem.pk)
        .select_related("categoria")
    )
    if categorias:
        base = base.filter(categoria__in=categorias)

    saldo = viagem.saldo_restante
    vistos = set()
    sugestoes = []

    for atracao in base[:40]:
        if atracao.nome in vistos:
            continue
        vistos.add(atracao.nome)
        sugestoes.append(
            {
                "nome": atracao.nome,
                "endereco": atracao.endereco,
                "categoria": atracao.categoria.slug,
                "categoria_nome": atracao.categoria.nome,
                "custo_estimado": atracao.custo_estimado,
                "tempo_estimado_horas": atracao.tempo_estimado_horas,
                "api_external_id": atracao.api_external_id,
                "distancia": None,
                "cabe_no_orcamento": atracao.custo_estimado <= saldo,
            }
        )

    return sugestoes


def obter_sugestoes(viagem, slugs=None, raio_m=None, limite=20):
    categorias = list(Categoria.objects.all())
    if slugs:
        categorias = [c for c in categorias if c.slug in slugs]

    if not categorias:
        return {"fonte": "local", "sugestoes": [], "aviso": "Nenhuma categoria selecionada."}

    try:
        if viagem.destino_lat is None or viagem.destino_lon is None:
            local = geocodificar(viagem.destino)
            viagem.destino_lat = local["lat"]
            viagem.destino_lon = local["lon"]
            viagem.save(update_fields=["destino_lat", "destino_lon"])

        tipos = []
        for categoria in categorias:
            tipos.extend(categoria.lista_geoapify)

        lugares = buscar_lugares(
            viagem.destino_lat, viagem.destino_lon, tipos, raio_m=raio_m, limite=limite
        )
    except ErroServicoExterno as erro:
        return {
            "fonte": "local",
            "sugestoes": _sugestoes_locais(viagem, categorias),
            "aviso": str(erro),
        }

    saldo = viagem.saldo_restante
    ja_salvos = set(
        viagem.atracoes.exclude(api_external_id="").values_list("api_external_id", flat=True)
    )

    sugestoes = []
    for lugar in lugares:
        if lugar["api_external_id"] and lugar["api_external_id"] in ja_salvos:
            continue
        categoria = _categoria_por_lugar(lugar, categorias)
        if categoria is None:
            continue
        sugestoes.append(_montar_sugestao(lugar, categoria, saldo))

    sugestoes.sort(key=lambda s: (s["distancia"] is None, s["distancia"] or 0))

    return {"fonte": "externa", "sugestoes": sugestoes, "aviso": ""}


def calcular_relatorio(viagem):
    atracoes = list(viagem.atracoes.select_related("categoria"))

    gastos = {}
    for atracao in atracoes:
        slug = atracao.categoria.slug
        gastos[slug] = gastos.get(slug, Decimal("0.00")) + atracao.custo_estimado

    custo_total = sum(gastos.values(), Decimal("0.00"))

    return {
        "viagem_id": viagem.pk,
        "destino": viagem.destino,
        "orcamento_total": viagem.orcamento_total,
        "custo_total_estimado": custo_total,
        "saldo_restante": viagem.orcamento_total - custo_total,
        "total_atracoes": len(atracoes),
        "gastos_por_categoria": gastos,
    }
