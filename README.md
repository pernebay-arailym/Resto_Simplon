# Resto_Simplon

Ordering system for a restaurant.

## Using Docker

### For developpement

```bash
docker compose -f ./compose_dev.yaml --env-file .env.dev up --build -d
```

#### Config files for **developpement** :

- .env.dev (see *Environnement file* section below)
- config_pgadmin_dev.json

In developpement, neither FastAPI nor Alembic are automatically run.

In api_dev container :

```bash
pip install -r requirements.txt
# SQL tables creation
alembic upgrade head
# Dev server for FastAPI :
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### For production

```bash
docker compose -f ./compose_prod.yaml --env-file .env.prod up --build -d
```

#### Config files for **production** :

- .env.prod (see *Environnement file* section below)
- config_pgadmin_prod.json

### Environnement file

The .env.dev and .env.prod files must follow this structure :

```
# Variables for fastAPI and PostgreSQL
JWT_SECRET=miohuyytftyyiuygvyucdtyedxty
# For JWT_ALGORITHM, keep the default value unless you know what you do…
JWT_ALGORITHM=HS256
POSTGRES_USER=db_user
POSTGRES_DB=resto_simplon
POSTGRES_PASSWORD=mypassword
# Replace THE_SERVER with the value: psql_dev in dev or the value: psql_prod in prod…
DATABASE_URL="postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@THE_SERVER:5432/${POSTGRES_DB}"
# Variables for pgAdmin
PGADMIN_DEFAULT_EMAIL=example@example.com
PGADMIN_DEFAULT_PASSWORD=mypassword
```