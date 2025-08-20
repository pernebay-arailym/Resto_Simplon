# 🍽️ Resto_Simplon

Ordering and management system for a restaurant, built with **FastAPI**, **PostgreSQL**, and **Docker**.  
This project was developed between **August 4 – 22, 2025** as part of an intensive Data Engineer formation, by a group of 3 members - @cebdewaelle, @alexishs, @pernebay-arailym.

---

## 📌 Project Overview

**Business Need**  
The client, *RestauSimplon*, wanted to digitalize the management of restaurant orders, previously handled on paper (leading to frequent errors and delays).

**Our Mission**  
Deliver a secure, tested, and containerized **REST API** for:  
- Authentication & Authorization with **JWT**  
- Menu management (**CRUD** for articles)  
- Customer management (**CRUD** for clients)  
- Order management (create, consult, filter, update status)  
- Database migrations with **Alembic**  
- Containerization with **Docker & Docker Compose**  
- Automated tests & CI/CD pipeline with **GitHub Actions**

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLAlchemy/SQLModel, Pydantic v2  
- **Database:** PostgreSQL, Alembic (migrations)  
- **Auth:** OAuth2 Password flow with JWT (access & refresh tokens)  
- **Containerization:** Docker, Docker Compose  
- **CI/CD:** GitHub Actions, pytest  
- **Other tools:** pgAdmin, bcrypt (hashing), PyJWT  

---

## 🚀 Installation & Usage

We provide **two environments**:  
- **Development** → local development with hot reload & manual migrations  
- **Production** → stable environment for deployment  

## 🔧 Development Setup

Start services with Docker Compose:

```
docker compose -f ./compose_dev.yaml --env-file .env.dev up --build -d
```

In the api_dev container:

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run Alembic migrations to create tables
```bash
alembic upgrade head
```

### Start FastAPI with hot reload
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🏭 Production Setup
```
docker compose -f ./compose_prod.yaml --env-file .env.prod up --build -d
```

In production, containers handle both API and migrations automatically.

## ⚙️ Environment Files

The .env.dev and .env.prod files must be created at the project root.

Example:

### JWT configuration
```
JWT_SECRET=supersecretkey
JWT_ALGORITHM=HS256
JWT_TOKEN_EXPIRES=3600  # in seconds
```

### PostgreSQL configuration
```
POSTGRES_USER=db_user
POSTGRES_DB=resto_simplon
POSTGRES_PASSWORD=mypassword
DATABASE_URL="postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@THE_SERVER:5432/${POSTGRES_DB}"
```

### pgAdmin credentials
```
PGADMIN_DEFAULT_EMAIL=example@example.com
PGADMIN_DEFAULT_PASSWORD=mypassword
```

- Use psql_dev as THE_SERVER for dev
- Use psql_prod as THE_SERVER for prod

## 🗄️ pgAdmin Config Files

The config_pgadmin_dev.json and config_pgadmin_prod.json files configure pgAdmin connections.

Example:
```
{
  "Servers": {
    "1": {
      "Name": "PostgreSQL Service",
      "Group": "Docker Servers",
      "Port": 5432,
      "Username": "db_user",
      "Host": "psql_dev",
      "SSLMode": "prefer",
      "MaintenanceDB": "resto_simplon"
    }
  }
}
```

## 📑 Database Migrations

We use Alembic for database schema migrations.

### Run migrations manually in dev:
- alembic upgrade head

### Generate a new migration:
- alembic revision --autogenerate -m "description"

## 🔐 Authentication

- Implemented with JWT tokens (OAuth2 Password flow).
- Roles: admin, employee, client
- Security: bcrypt hashing, refresh & access tokens, configurable expiry

## 🛒 Orders & Status Enum

Orders are created by clients (for themselves) or staff (for any client).
The system automatically calculates the total price.

Order Status Workflow

We defined a 6-state enumeration:

```
class OrderStatus(str, Enum):
    CREATED = "Created"
    PREPARING = "Preparing"
    READY = "Ready"
    SERVED = "Served"
    CANCELLED = "Cancelled"
    PAID = "Paid"
```

## 🧪 Testing

We use pytest for unit and integration tests.

Run all tests:

``` bash
pytest
```
Run tests with coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

## 🔄 CI/CD

We implemented GitHub Actions at .github/workflows/ci.yaml:

Pipeline tasks:

1. Install dependencies
2. Run linting and tests (pytest, coverage ≥ 80%)
3. Build Docker images
4. Push images to registry
5. Deploy

The CI/CD pipeline runs on every push and pull request, ensuring code quality and deployment readiness.

## 📖 API Documentation

FastAPI automatically generates documentation:

Swagger UI → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

## 📜 License

This project is licensed under the MIT License. See LICENSE for details.

## 👥 Authors

Project completed during Data Engineer Intensive Formation (3 weeks, Aug 2025).