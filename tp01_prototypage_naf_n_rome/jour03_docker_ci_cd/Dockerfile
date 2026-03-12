# ==================================================
# Stage 1 : Builder -- installe les dépendances
# ==================================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Installe uv pour une installation rapide des dépendances
RUN pip install --no-cache-dir uv==0.5.0

# Copie uniquement les fichiers de dépendances
COPY pyproject.toml .

# Installe les dépendances dans un répertoire dédié
RUN uv pip install --system --no-cache \
    fastapi uvicorn[standard] pydantic pydantic-settings pandas structlog httpx

# ==================================================
# Stage 2 : Runtime -- image finale légère
# ==================================================
FROM python:3.12-slim AS runtime

# Métadonnées
LABEL maintainer="CreativeTech"
LABEL description="API NAF-ROME - TP Master IA"

# Crée un utilisateur non-root (sécurité)
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copie les packages Python installés depuis le builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copie le code applicatif
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup data/ ./data/

# Passe à l'utilisateur non-root
USER appuser

# Expose le port
EXPOSE 8000

# Healthcheck Docker natif
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
