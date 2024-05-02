FROM python:3.12.3-alpine3.19
LABEL authors="Bohdan Salamakha"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --with prod

COPY . .
RUN mkdir static && mkdir media && chmod +x entrypoint.sh

EXPOSE 8000
