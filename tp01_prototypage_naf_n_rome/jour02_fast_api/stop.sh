#!/usr/bin/env bash
# Arrête l'API FastAPI (port 8000)

PORT=8000
PID=$(lsof -ti tcp:$PORT 2>/dev/null)

if [ -z "$PID" ]; then
  echo "Aucun serveur trouvé sur le port $PORT."
else
  echo "Arrêt de l'API (PID $PID) sur le port $PORT..."
  kill "$PID" 2>/dev/null && echo "API arrêtée." || echo "Impossible d'arrêter le processus."
fi
