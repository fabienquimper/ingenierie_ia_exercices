#!/usr/bin/env bash
set -e

echo "=== NAF-ROME Frontend — Jour 1 (CSV) ==="
echo ""

# Sur WSL + filesystem Windows (/mnt/c/), l'interop peut faire appel au node
# Windows au lieu du node WSL. On force le node Linux explicitement.
WSL_NODE=$(which -a node 2>/dev/null | grep -v "/mnt/" | head -1)
NODE="${WSL_NODE:-node}"

echo "Node : $($NODE --version) — $NODE"
echo ""

# Installe les dépendances si vite est absent
if [ ! -f "node_modules/.bin/vite" ]; then
  echo "Installation des dépendances npm..."
  npm install
  echo ""
fi

echo "Démarrage du serveur de développement..."
echo "URL : http://localhost:5173"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter."
echo ""

# Appel direct au node WSL + vite.js (contourne l'interop Windows)
exec "$NODE" ./node_modules/vite/bin/vite.js
