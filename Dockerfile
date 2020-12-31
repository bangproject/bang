FROM python:3.9.0-slim-buster

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .
