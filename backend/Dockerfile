FROM python:3.11-slim

WORKDIR /app/

ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME=/usr/local \
    POETRY_VIRTUALENVS_CREATE=false

RUN BUILD_DEPS="curl build-essential gcc libpq-dev" && \
    apt-get update && \
    apt-get install --no-install-recommends -y $BUILD_DEPS


RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

ENV PYTHONPATH=/app

COPY ./app /app/app

ENV APP_NAME=QAAaaS
ENV APP_ENVIRONMENT=development
LABEL name="QAAaaS" \
      version="0.1.0"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
