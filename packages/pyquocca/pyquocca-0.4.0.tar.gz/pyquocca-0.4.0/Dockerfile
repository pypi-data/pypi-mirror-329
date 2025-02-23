FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app
COPY . .

RUN uv sync --all-extras

ENTRYPOINT []
# CMD sleep 5 && .venv/bin/python3 src/test_app/main.py
CMD sleep 5 && .venv/bin/gunicorn -c python:pyquocca.gunicorn test_app.main:app