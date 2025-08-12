# Utilise une image Python
FROM python:slim-bookworm

# Définis le répertoire de travail dans le conteneur
WORKDIR /app_base
RUN cd /app_base

# Copie les fichiers de configuration et d'exigences
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste de ton application et les fichiers de migration
COPY alembic ./alembic
COPY app ./app
COPY alembic.ini .
COPY .env .

EXPOSE 8000

COPY fastapi_image/entry_point.sh .
RUN chmod +x ./entry_point.sh

# Définit le script comme point d'entrée du conteneur
ENTRYPOINT ["./entry_point.sh"]
CMD [""]