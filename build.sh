#!/usr/bin/env bash
# Build command do Render. Roda a cada deploy.
set -o errexit

pip install --no-cache-dir -r requirements.txt

# Arquivos estaticos servidos pelo WhiteNoise
python manage.py collectstatic --no-input

# Esquema do banco (Supabase Postgres via pooler em session mode)
python manage.py migrate --no-input

# Tabela usada pelo DatabaseCache (idempotente)
python manage.py createcachetable

# Dados de apoio (idempotentes)
python manage.py seed_categorias
python manage.py criar_superuser
