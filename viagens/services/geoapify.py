import hashlib
import logging
import unicodedata

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

URL_GEOCODE = "https://api.geoapify.com/v1/geocode/search"
URL_PLACES = "https://api.geoapify.com/v2/places"

CONFIANCA_MINIMA = 0.4


class ErroServicoExterno(Exception):
    pass


class TimeoutServicoExterno(ErroServicoExterno):
    pass


class LimiteServicoExterno(ErroServicoExterno):
    pass


class DestinoNaoEncontrado(Exception):
    pass


def _normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto or "")
    sem_acento = sem_acento.encode("ascii", "ignore").decode("ascii")
    return " ".join(sem_acento.lower().split())


def _chave_cache(prefixo, *partes):
    bruto = "|".join(str(p) for p in partes)
    assinatura = hashlib.sha256(bruto.encode("utf-8")).hexdigest()[:32]
    return f"geoapify:{prefixo}:{assinatura}"


def _requisitar(url, params):
    if not settings.GEOAPIFY_API_KEY:
        raise ErroServicoExterno("GEOAPIFY_API_KEY nao configurada.")

    try:
        resposta = requests.get(
            url,
            params=params,
            headers={"x-api-key": settings.GEOAPIFY_API_KEY},
            timeout=settings.GEOAPIFY_TIMEOUT,
        )
    except requests.Timeout:
        logger.warning("Timeout ao consultar %s", url)
        raise TimeoutServicoExterno("A busca demorou demais para responder.")
    except requests.RequestException:
        logger.warning("Falha de conexao ao consultar %s", url)
        raise ErroServicoExterno("Nao foi possivel conectar ao servico de busca.")

    if resposta.status_code == 429:
        raise LimiteServicoExterno("Limite de consultas atingido. Tente mais tarde.")

    if resposta.status_code in (401, 403):
        logger.error("Chave da Geoapify recusada (HTTP %s).", resposta.status_code)
        raise ErroServicoExterno("Servico de busca indisponivel.")

    if resposta.status_code >= 500:
        raise ErroServicoExterno("O servico de busca esta instavel.")

    if resposta.status_code != 200:
        raise ErroServicoExterno("Resposta inesperada do servico de busca.")

    try:
        return resposta.json()
    except ValueError:
        raise ErroServicoExterno("O servico de busca retornou dados invalidos.")


def geocodificar(destino):
    destino_normalizado = _normalizar(destino)
    if not destino_normalizado:
        raise DestinoNaoEncontrado("Informe um destino.")

    chave = _chave_cache("geocode", destino_normalizado)
    guardado = cache.get(chave)
    if guardado is not None:
        return guardado

    dados = _requisitar(
        URL_GEOCODE,
        {
            "text": destino,
            "type": "city",
            "lang": "pt",
            "limit": 1,
            "filter": "countrycode:br",
            "format": "json",
        },
    )

    resultados = dados.get("results") or []
    if not resultados:
        raise DestinoNaoEncontrado("Nao encontramos esse destino.")

    primeiro = resultados[0]
    confianca = (primeiro.get("rank") or {}).get("confidence") or 0
    if confianca < CONFIANCA_MINIMA:
        raise DestinoNaoEncontrado("Nao encontramos esse destino com precisao.")

    local = {
        "lat": primeiro.get("lat"),
        "lon": primeiro.get("lon"),
        "formatado": primeiro.get("formatted") or destino,
    }
    cache.set(chave, local, settings.GEOAPIFY_CACHE_TTL)
    return local


def buscar_lugares(lat, lon, categorias, raio_m=None, limite=20):
    if not categorias:
        return []

    raio_m = raio_m or settings.GEOAPIFY_RAIO_PADRAO_M
    categorias_ordenadas = ",".join(sorted(categorias))

    chave = _chave_cache("places", lat, lon, categorias_ordenadas, raio_m, limite)
    guardado = cache.get(chave)
    if guardado is not None:
        return guardado

    dados = _requisitar(
        URL_PLACES,
        {
            "categories": categorias_ordenadas,
            "filter": f"circle:{lon},{lat},{raio_m}",
            "bias": f"proximity:{lon},{lat}",
            "limit": limite,
            "lang": "pt",
        },
    )

    lugares = []
    for item in dados.get("features") or []:
        propriedades = item.get("properties") or {}
        nome = propriedades.get("name")
        if not nome:
            continue
        lugares.append(
            {
                "nome": nome[:255],
                "endereco": (propriedades.get("address_line2") or propriedades.get("formatted") or "")[:255],
                "categorias": propriedades.get("categories") or [],
                "api_external_id": propriedades.get("place_id") or "",
                "distancia": propriedades.get("distance"),
            }
        )

    cache.set(chave, lugares, settings.GEOAPIFY_CACHE_TTL)
    return lugares
