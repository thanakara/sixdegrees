FROM python:3.13-slim@sha256:d49c1ff87eb98eac346fc250f52925f726eb913c43a92854246dd03c9692ad67 AS build

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY sixdegrees/ ./sixdegrees/
COPY wsgi.py ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.13-slim@sha256:d49c1ff87eb98eac346fc250f52925f726eb913c43a92854246dd03c9692ad67 AS runtime

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN useradd --system --no-create-home nonroot

COPY --from=build /app/.venv /app/.venv
COPY --chown=nonroot:nonroot --from=build /app/sixdegrees /app/sixdegrees
COPY --chown=nonroot:nonroot --from=build /app/wsgi.py /app/wsgi.py

USER nonroot

WORKDIR /app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "wsgi:app"]
