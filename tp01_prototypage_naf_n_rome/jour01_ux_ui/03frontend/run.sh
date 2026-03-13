#!/usr/bin/env bash
set -e

echo "=== NAF-ROME Frontend — Jour 1 (CSV) ==="
echo ""

# ── 1. Trouver node + npm Linux (nvm en priorité) ─────────────────────────────
#
# Problème WSL : npm est celui de Windows (/mnt/c/...) et installe des binaires
# win32 (esbuild, rollup) que le node Linux ne peut pas charger.
# Solution : utiliser le node/npm natif Linux installé via nvm.
#
NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

# Cherche la première version node nvm installée (triée par version décroissante)
NVM_NODE=$(ls -d "$NVM_DIR/versions/node"/*/bin/node 2>/dev/null \
           | sort -t/ -k7 -V -r | head -1)

if [ -n "$NVM_NODE" ] && [ -x "$NVM_NODE" ]; then
  NODE="$NVM_NODE"
  NVM_BIN="$(dirname "$NVM_NODE")"
else
  # Fallback : premier node WSL hors /mnt/
  WSL_NODE=$(which -a node 2>/dev/null | grep -v "/mnt/" | head -1)
  NODE="${WSL_NODE:-node}"
  NVM_BIN=""
fi

# Préfixer PATH avec le bin nvm pour que le shebang "#!/usr/bin/env node"
# de npm/vite utilise aussi notre node Linux
if [ -n "$NVM_BIN" ]; then
  export PATH="$NVM_BIN:$PATH"
fi

echo "Node : $($NODE --version) — $NODE"
echo "npm  : $(npm --version) — $(which npm)"
echo ""

# ── 2. Installer les dépendances si vite est absent ───────────────────────────
if [ ! -f "node_modules/.bin/vite" ]; then
  echo "Installation des dépendances npm (Linux natif)..."
  npm install
  echo ""
fi

# ── 3. Lancer Vite ────────────────────────────────────────────────────────────
echo "Démarrage du serveur de développement..."
echo "URL : http://localhost:5173"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter."
echo ""

exec node ./node_modules/vite/bin/vite.js
