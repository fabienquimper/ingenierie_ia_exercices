#!/usr/bin/env bash
set -e

echo "=== NAF-ROME Frontend — Jour 1 (CSV) ==="
echo ""

# Installe les dépendances si node_modules absent
if [ ! -d "node_modules" ]; then
  echo "Installation des dépendances npm..."
  npm install
  echo ""
fi

echo "Démarrage du serveur de développement..."
echo "URL : http://localhost:5173"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter."
echo ""

npm run dev
