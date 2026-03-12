#!/usr/bin/env bash
set -e

echo "=== NAF-ROME Frontend — Jour 2 (API FastAPI) ==="
echo ""

# Installe les dépendances si node_modules absent
if [ ! -d "node_modules" ]; then
  echo "Installation des dépendances npm..."
  npm install
  echo ""
fi

# Vérifie que l'API est joignable
API_URL="${VITE_API_URL:-http://localhost:8000}"
echo "Vérification de l'API sur $API_URL/health ..."
if curl -sf "$API_URL/health" > /dev/null 2>&1; then
  echo "  API connectée ✓"
else
  echo "  ⚠️  L'API semble hors ligne."
  echo "     Lancez d'abord : cd .. && ./run.sh"
  echo "     (le frontend démarrera quand même)"
fi
echo ""

echo "Démarrage du serveur de développement..."
echo "URL  : http://localhost:5174"
echo "API  : $API_URL"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter."
echo ""

npm run dev
