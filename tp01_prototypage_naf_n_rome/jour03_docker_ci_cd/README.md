# TP 1.2 — Docker & CI/CD : Déploiement de l'API NAF-ROME

## Description

Ce TP vous guide pour containeriser et déployer l'API FastAPI de correspondance NAF/ROME
avec Docker, docker-compose et un pipeline CI/CD GitHub Actions.

**Durée estimée :** 1 journée (7h)

---

## Prérequis

- Python 3.12+
- Docker Desktop (ou Docker Engine)
- Git

---

## Démarrage rapide

### Option 1 : Lancement local (sans Docker)

```bash
# Installer les dépendances
pip install -e ".[dev]"

# Lancer l'API
uvicorn app.main:app --reload --port 8000
```

L'API est disponible sur : http://localhost:8000
Documentation Swagger : http://localhost:8000/docs

### Option 2 : Lancement avec Docker Compose (recommandé)

```bash
# Construire et démarrer tous les services
docker compose up --build

# En arrière-plan
docker compose up --build -d

# Voir les logs
docker compose logs -f api

# Arrêter
docker compose down
```

### Option 3 : Docker seul

```bash
# Construire l'image
docker build -t naf-rome-api:local .

# Lancer le conteneur
docker run -p 8000:8000 -v $(pwd)/data:/app/data:ro naf-rome-api:local
```

---

## Endpoints de l'API

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Page d'accueil |
| GET | `/health` | Vérification de santé |
| GET | `/metrics` | Métriques (format Prometheus simplifié) |
| GET | `/docs` | Documentation Swagger interactive |
| GET | `/api/v1/rome` | Lister les codes ROME (paginé) |
| GET | `/api/v1/rome/{code}` | Détail d'un code ROME |
| GET | `/api/v1/naf` | Lister les codes NAF (paginé) |
| GET | `/api/v1/naf/{code}` | Détail d'un code NAF |
| POST | `/api/v1/search` | Recherche par mots-clés |
| GET | `/api/v1/mapping/rome-to-naf/{code}` | Correspondances ROME -> NAF |
| GET | `/api/v1/mapping/naf-to-rome/{code}` | Correspondances NAF -> ROME |

### Exemples curl

```bash
# Santé de l'API
curl http://localhost:8000/health

# Lister les codes ROME
curl "http://localhost:8000/api/v1/rome?limit=5"

# Recherche par mot-clé
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "informatique", "limit": 5}'

# Correspondance NAF vers ROME
curl http://localhost:8000/api/v1/mapping/naf-to-rome/62.01Z

# Correspondance ROME vers NAF
curl http://localhost:8000/api/v1/mapping/rome-to-naf/M1805
```

---

## Lancer les tests

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture de code
pytest tests/ -v --cov=app --cov-report=term-missing

# Un seul fichier
pytest tests/test_health.py -v

# Avec rapport HTML
pytest tests/ --cov=app --cov-report=html
# Ouvrir htmlcov/index.html
```

---

## Structure du projet

```
jour03_docker_ci_cd/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration via variables d'environnement
│   ├── main.py            # Point d'entrée FastAPI
│   ├── models.py          # Schémas Pydantic
│   ├── routers/
│   │   ├── health.py      # Routes /health et /metrics
│   │   └── mapping.py     # Routes /api/v1/...
│   └── services/
│       └── matcher.py     # Logique métier NAF/ROME
├── data/
│   └── sample_naf_rome.csv  # Données d'exemple (40 entrées)
├── tests/
│   ├── conftest.py        # Fixtures pytest
│   ├── test_health.py     # Tests endpoints de santé
│   └── test_mapping.py    # Tests endpoints de mapping
├── .github/
│   └── workflows/
│       └── ci.yml         # Pipeline CI/CD GitHub Actions
├── .dockerignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile             # Multi-stage build
└── pyproject.toml
```

---

## Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `APP_DEBUG` | `false` | Mode debug |
| `APP_DATA_PATH` | `data/sample_naf_rome.csv` | Chemin vers les données |
| `APP_CORS_ORIGINS` | `["*"]` | Origines CORS autorisées |

---

## Objectifs pédagogiques

### A. Containerisation Docker
- [ ] Comprendre la structure d'un Dockerfile multi-stage
- [ ] Optimiser la taille de l'image (builder vs runtime)
- [ ] Utiliser un utilisateur non-root pour la sécurité
- [ ] Configurer le HEALTHCHECK Docker

### B. Docker Compose
- [ ] Orchestrer plusieurs services (API + Redis)
- [ ] Gérer les dépendances entre services (`depends_on`)
- [ ] Monter des volumes pour les données
- [ ] Configurer les réseaux Docker

### C. CI/CD avec GitHub Actions
- [ ] Créer un pipeline en 3 étapes : Lint -> Test -> Build
- [ ] Publier une image Docker sur GitHub Container Registry (GHCR)
- [ ] Utiliser le cache Docker pour accélérer les builds
- [ ] Configurer les permissions et secrets GitHub

### D. Qualité du code
- [ ] Utiliser Ruff pour le linting et le formatage
- [ ] Configurer pre-commit hooks
- [ ] Atteindre 70%+ de couverture de tests

---

## Exercices d'extension

### Niveau 1 : Amélioration de l'API
1. Ajouter un endpoint `GET /api/v1/stats` retournant des statistiques sur les données
2. Implémenter le filtre par type (`?type=naf` ou `?type=rome`) dans la liste
3. Ajouter la validation des codes NAF (format: `\d{2}\.\d{2}[A-Z]`)

### Niveau 2 : Cache Redis
1. Intégrer `redis-py` pour cacher les résultats de recherche
2. Ajouter un TTL de 5 minutes sur les entrées du cache
3. Exposer un endpoint `DELETE /cache` pour vider le cache

### Niveau 3 : Monitoring avancé
1. Intégrer `prometheus-fastapi-instrumentator` pour les métriques réelles
2. Ajouter Grafana dans le docker-compose pour visualiser les métriques
3. Configurer des alertes sur le taux d'erreur

### Niveau 4 : Recherche sémantique
1. Intégrer `sentence-transformers` pour la recherche vectorielle
2. Pré-calculer les embeddings au démarrage
3. Comparer les performances : keyword vs sémantique

---

## Dépannage

### L'API ne démarre pas
```bash
# Vérifier les logs
docker compose logs api

# Vérifier que le fichier de données existe
ls -la data/

# Tester sans Docker
python -c "from app.main import app; print('OK')"
```

### Erreur de permission Docker
```bash
# Sur Linux, ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
# Puis se déconnecter/reconnecter
```

### Les tests échouent
```bash
# Vérifier l'installation
pip install -e ".[dev]"

# Lancer un test spécifique avec plus de détails
pytest tests/test_health.py -v -s
```
