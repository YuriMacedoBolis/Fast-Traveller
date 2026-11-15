from datetime import datetime
from decimal import Decimal, InvalidOperation

from rest_framework.exceptions import ValidationError


def _decimal(valor, campo):
    try:
        return Decimal(valor)
    except (InvalidOperation, TypeError):
        raise ValidationError({campo: "Informe um valor numérico válido."})


def _inteiro(valor, campo):
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ValidationError({campo: "Informe um número inteiro válido."})


def _data(valor, campo):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValidationError({campo: "Use o formato AAAA-MM-DD."})


def aplicar_filtros(queryset, params):
    destino = params.get("destino")
    if destino:
        queryset = queryset.filter(destino__icontains=destino.strip())

    orcamento_min = params.get("orcamento_min")
    if orcamento_min:
        queryset = queryset.filter(
            orcamento_total__gte=_decimal(orcamento_min, "orcamento_min")
        )

    orcamento_max = params.get("orcamento_max")
    if orcamento_max:
        queryset = queryset.filter(
            orcamento_total__lte=_decimal(orcamento_max, "orcamento_max")
        )

    data_apos = params.get("data_inicio_apos")
    if data_apos:
        queryset = queryset.filter(data_inicio__gte=_data(data_apos, "data_inicio_apos"))

    data_antes = params.get("data_inicio_antes")
    if data_antes:
        queryset = queryset.filter(data_inicio__lte=_data(data_antes, "data_inicio_antes"))

    duracao_min = params.get("duracao_min")
    if duracao_min:
        queryset = queryset.filter(duracao_dias__gte=_inteiro(duracao_min, "duracao_min"))

    duracao_max = params.get("duracao_max")
    if duracao_max:
        queryset = queryset.filter(duracao_dias__lte=_inteiro(duracao_max, "duracao_max"))

    return queryset
