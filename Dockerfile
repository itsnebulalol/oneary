FROM python:3.12.3-slim-bullseye as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    # paths
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/env" \
    ONEARY_HOME="/app/config"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

## Builder stage
FROM base as builder
RUN apt-get update && apt-get install --no-install-recommends -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY oneary ./oneary
COPY LICENSE README.md main.py pyproject.toml poetry.lock ./

RUN poetry build --format wheel
RUN python -m venv env
RUN pip install dist/*.whl

## Main stage
FROM base as main

COPY --from=builder $VENV_PATH $VENV_PATH
RUN mkdir $ONEARY_HOME

ENTRYPOINT [ "oneary" ]