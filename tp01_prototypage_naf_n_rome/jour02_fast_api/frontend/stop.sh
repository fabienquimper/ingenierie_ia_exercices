#!/usr/bin/env bash
# Arrête le serveur de développement Vite (port 5174)

PORT=5174
PID=$(lsof -ti tcp:$PORT 2>/dev/null)

if [ -z "$PID" ]; then
  echo "Aucun serveur trouvé sur le port $PORT."
else
  echo "Arrêt du serveur (PID $PID) sur le port $PORT..."
  kill "$PID" 2>/dev/null && echo "Serveur arrêté." || echo "Impossible d'arrêter le processus."
fi
