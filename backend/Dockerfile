FROM python:3.13-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH=/code

RUN apt update && apt install -y curl && apt clean

RUN pip install --upgrade pip setuptools \
    && pip install poetry

COPY ./pyproject.toml /code/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./backend/app /code/app
COPY ./backend/gunicorn_conf.py /gunicorn_conf.py

COPY ./backend/scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./backend/scripts/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80
CMD [ "/start.sh" ]