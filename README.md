# E-Commerce Project

An example e-commerce backend built with **FastAPI**, **Celery** (for background tasks), **PostgreSQL**, and **Redis**.

## Requirements

- [Docker](https://docs.docker.com/get-docker/) installed  
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Project Structure

```bash
.
├── docker-compose.yml
├── .env
├── Dockerfile
├── requirements.txt
├── src/
│   ├── main.py         # FastAPI entry point
│   ├── celery_app.py   # Celery initialization
│   ├── ...
└── README.md
```

## Environment Variables (.env)

In the project root, create (or edit) a file named `.env`. For example:

```bash
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ecommerce_db
POSTGRES_SCHEMA=public

REDIS_HOST=redis
REDIS_PORT=6379

CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

> Leave these deafult values to run in Docker. If any variables are omitted, the **default** values in `docker-compose.yml` are used (e.g., `6379` for Redis, `5432` for Postgres).

## How It Works

1. The `migrate` service runs database migrations (e.g., `alembic upgrade head`) **once** and exits.
2. The `api` service **depends** on `migrate`, ensuring that migrations are applied before the API starts.
3. The `celery` service connects to Redis and Postgres for background tasks.

## Running the Project

1. Ensure your `.env` file is properly set.
2. Run:

   ```bash
   docker-compose up --build
   ```

   After images are built and containers start, you will see logs for:
   - `migrate` (runs migrations then exits)
   - `db-postgres` (PostgreSQL)
   - `redis` (Redis)
   - `api` (FastAPI on port 8000)
   - `celery` (Celery worker)

3. **Check logs**:
   - The `migrate` container should run `alembic upgrade head` (or your chosen migration tool) and exit with code 0 if successful.
   - `api` depends on `migrate`, so it will only start after the database is migrated.

4. Access the FastAPI application at [http://localhost:8000](http://localhost:8000).  
   You can also view the auto-generated docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Services

- **migrate**  
  A one-shot service that runs migrations (`alembic upgrade head`) and exits. Ensures your DB schema is up to date before starting the app.

- **db-postgres**  
  Runs PostgreSQL. Credentials and port come from `.env` (or default values).

- **redis**  
  Runs Redis, which Celery uses as the message broker and results backend.

- **api**  
  Runs the FastAPI application on port 8000. Depends on `migrate` (thus also on `db-postgres` and `redis`).

- **celery**  
  A container running Celery worker. Depends on `redis` (for broker/backend) and `db-postgres` if tasks need DB access.

## Usage

- After the containers are up, you can create or list products, orders, and so on.
- For background tasks (Celery), your code will publish tasks to Redis. The `celery` service will process them in the background.

## Stopping

Press `Ctrl + C` where `docker-compose up` is running, or:

```bash
docker-compose down
```

This stops and removes the containers, but preserves any named volumes (such as PostgreSQL data).
