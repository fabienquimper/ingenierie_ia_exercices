#!/bin/bash
# ===========================================================
# run.sh -- Script de démarrage de l'API NAF-ROME
# TP 1.1 -- FastAPI
# ===========================================================

set -e  # Arrête le script en cas d'erreur

echo "=== NAF-ROME API - Démarrage ==="
echo ""

# Vérifie que Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python: $PYTHON_VERSION"

# Crée un environnement virtuel si nécessaire
if [ ! -d ".venv" ]; then
    echo ""
    echo "Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Active l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installe les dépendances si nécessaire
if ! python -c "import fastapi" &> /dev/null 2>&1; then
    echo ""
    echo "Installation des dépendances..."
    pip install -e "." --quiet
fi

# Vérifie que le fichier de données existe
if [ ! -f "data/sample_naf_rome.csv" ]; then
    echo "ERREUR: Le fichier data/sample_naf_rome.csv est introuvable."
    echo "Vérifiez que vous êtes dans le bon répertoire."
    exit 1
fi

echo ""
echo "=== Démarrage du serveur ==="
echo "URL: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "Santé: http://localhost:8000/health"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter."
echo ""

# Lance l'API avec rechargement automatique (mode développement)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
