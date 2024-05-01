FROM ubuntu:23.10
LABEL authors="Bohdan Salamakha"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python-is-python3 gcc curl ca-certificates \
    && curl https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --with prod

COPY . .
RUN mkdir static

EXPOSE 8000
