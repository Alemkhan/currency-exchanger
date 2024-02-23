FROM python:3.11-slim as builder
WORKDIR /app

RUN apt-get update && apt-get install -y curl git
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH=$PATH:/etc/poetry/bin

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.in-project true

RUN poetry install --only main
RUN poetry add uvloop

FROM python:3.11-slim as app
WORKDIR /app
ENV PYTHONPATH=$PYTHONPATH:/app/src PATH=/app/.venv/bin:$PATH
COPY --from=builder /app/.venv .venv
COPY ./src ./src
COPY ./alembic ./alembic
COPY alembic.ini ./
ENTRYPOINT ["uvicorn", "--factory", "app:create_app", "--proxy-headers", "--loop", "uvloop", "--host", "0.0.0.0", "--port", "80"]

