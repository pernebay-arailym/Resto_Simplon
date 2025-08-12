# Utilise une image Python
FROM python:slim-bookworm

# Définis le répertoire de travail dans le conteneur
WORKDIR /app_base

# Librairies python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste de ton application et les fichiers de migration
COPY alembic ./alembic
COPY app ./app
COPY alembic.ini .

CMD ["alembic", "upgrade", "head"]