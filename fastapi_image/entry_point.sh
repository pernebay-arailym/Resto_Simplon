#!/bin/sh

# vérifier si cette ligne est nécessaire
cd /app_base

if [ ! -f "alembic_passe" ]; then
    echo "Exécution d'alembic…"
    alembic upgrade head
    touch alembic_passe
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload