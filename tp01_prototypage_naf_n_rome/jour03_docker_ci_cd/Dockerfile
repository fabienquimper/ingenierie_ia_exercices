# ==================================================
# Stage 1 : Builder -- installe les dépendances
# ==================================================
FROM python:3.12-slim AS builder

WORKDIR /build

RUN pip install --no-cache-dir uv==0.5.0

COPY pyproject.toml .

# Dépendances de production
RUN uv pip install --system --no-cache \
    fastapi uvicorn[standard] pydantic pydantic-settings pandas structlog httpx

# ==================================================
# Stage 2 : Test -- vérifie la qualité avant de packager
# (utilisé en CI : docker build --target test .)
# ==================================================
FROM builder AS test

WORKDIR /app

# Dépendances de dev uniquement pour ce stage
RUN uv pip install --system --no-cache \
    pytest pytest-cov pytest-asyncio httpx

COPY app/ ./app/
COPY tests/ ./tests/

RUN pytest tests/ -v --tb=short

# ==================================================
# Stage 3 : Runtime -- image finale légère
# ==================================================
FROM python:3.12-slim AS runtime

LABEL maintainer="CreativeTech"
LABEL description="API NAF-ROME - TP Master IA"

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup data/ ./data/

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
