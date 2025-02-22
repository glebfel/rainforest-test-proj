# syntax=docker/dockerfile:1.2

FROM python:3.11 AS builder

WORKDIR /app
ENV PYTHONBUFFERED=1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - \
    && ln -s /etc/poetry/bin/poetry /usr/local/bin/poetry
ENV PATH=$PATH:/etc/poetry/bin

# Configure Poetry
RUN poetry config virtualenvs.in-project true
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install
RUN poetry add uvloop

# Build final image
FROM python:3.11-slim AS final

WORKDIR /app

ENV PYTHONBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:/app/src PATH=/app/.venv/bin:$PATH

COPY --from=builder /app/.venv .venv
COPY . .

RUN chgrp -R 0 /app && chmod -R g=u /app

ENTRYPOINT ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000"]
