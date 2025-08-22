# Utilise une image Python
FROM python:slim-bookworm

RUN useradd -m app_user
USER app_user
ENV PATH="/home/app_user/.local/bin:${PATH}"

# Définis le répertoire de travail dans le conteneur
WORKDIR /app_base

# Librairies python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste de ton application et les fichiers de migration
COPY alembic ./alembic
COPY app ./app
COPY alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]