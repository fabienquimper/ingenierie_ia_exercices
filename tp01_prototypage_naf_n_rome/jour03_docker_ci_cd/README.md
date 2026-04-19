# TP 1.2 — Docker & CI/CD : Déploiement de l'API NAF-ROME

**Niveau :** Master IA · CreativeTech  
**Durée estimée :** 1 journée (7h)

---

## Progression pédagogique

Ce TP est la troisième étape d'une progression en 3 jours sur la même application NAF-ROME :

| | Jour 1 | Jour 2 | Jour 3 |
|---|---|---|---|
| **Technologie** | Vue.js + CSV | FastAPI + Vue.js | Docker + CI/CD |
| **Données** | 3 CSV dans le navigateur | 3 CSV via API Python | Idem Jour 2, containerisé |
| **Déploiement** | `vite dev` | `uvicorn` + `vite dev` | `docker compose up` (API) + `vite dev` (front) |
| **Tests** | Manuels | pytest local | pytest dans Docker (stage `test`) |
| **Reproductibilité** | Machine locale uniquement | Machine locale uniquement | N'importe quel environnement |

> **Ce que jour 3 apporte :** l'application tourne maintenant dans des conteneurs isolés, les tests font partie du build Docker, et un pipeline CI/CD vérifie automatiquement chaque commit.

---

## Prérequis

- Docker Desktop (ou Docker Engine + Docker Compose v2)
- Git
- Python 3.12+ et le `.venv` du Jour 2 (pour les tests locaux)

---

## Démarrage rapide

### Option 1 : Docker Compose (recommandé — approche Jour 3)

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

Vérifiez que tout est opérationnel :

```bash
# Conteneurs actifs et healthy
docker ps

# Santé de l'API + nombre d'enregistrements chargés
curl http://localhost:8000/health
# → {"status": "ok", "version": "1.0.0", "records_loaded": 23195}
```

| Service | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger (docs interactives) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### Accéder à l'application complète (frontend + API Docker)

Le frontend du Jour 2 peut se connecter à l'API qui tourne dans Docker **sans aucune modification** — Docker expose le port `8000` sur la machine hôte, le frontend l'utilise comme si c'était un `uvicorn` local.

```bash
# Terminal 1 — API dans Docker
docker compose up --build -d

# Terminal 2 — Frontend du Jour 2 (local, pointe sur localhost:8000)
cd ../jour02_fast_api/frontend
./run.sh
```

| Service | URL | Mode |
|---|---|---|
| API | http://localhost:8000 | Docker |
| Swagger | http://localhost:8000/docs | Docker |
| Frontend | http://localhost:5174 | Local (Jour 2) |

> **Point pédagogique clé :** le frontend ne "sait" pas que l'API tourne dans Docker. Il appelle `localhost:8000` — c'est l'API, peu importe comment elle est hébergée. C'est la promesse d'isolation de Docker.

### Option 2 : Docker seul

```bash
# Construire l'image complète (passe par le stage test automatiquement)
docker build -t naf-rome-api:local .

# Lancer uniquement le stage test (CI/CD)
docker build --target test -t naf-rome-api:test .

# Lancer le conteneur
docker run -p 8000:8000 -v $(pwd)/data:/app/data:ro naf-rome-api:local
```

### Option 3 : Local sans Docker (développement)

```bash
# Réutiliser le venv du Jour 2
source ../jour02_fast_api/.venv/bin/activate

# Lancer l'API
uvicorn app.main:app --reload --port 8000
```

---

## Le Dockerfile multi-stage (3 stages)

```
Builder ──► Test ──► Runtime
   │           │         │
   │     (pytest)   image finale
   │                 légère
   └── dépendances prod
```

| Stage | Rôle | Commande |
|---|---|---|
| `builder` | Installe les dépendances de production | (automatique) |
| `test` | Lance `pytest tests/` — bloque le build si un test échoue | `docker build --target test .` |
| `runtime` | Image finale légère, utilisateur non-root | `docker build .` |

> En CI/CD, le pipeline exécute `docker build --target test .` avant de publier l'image.  
> Si les tests échouent, l'image n'est jamais construite ni publiée.

---

## Endpoints de l'API

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Page d'accueil |
| GET | `/health` | Vérification de santé |
| GET | `/metrics` | Métriques (format Prometheus simplifié) |
| GET | `/docs` | Documentation Swagger interactive |
| GET | `/redoc` | Documentation ReDoc |
| GET | `/api/v1/naf` | Lister les codes NAF (paginé) |
| GET | `/api/v1/naf/{code}` | Détail d'un code NAF |
| GET | `/api/v1/rome` | Lister les codes ROME (paginé) |
| GET | `/api/v1/rome/{code}` | Détail d'un code ROME |
| GET | `/api/v1/matching` | Lister les correspondances NAF↔ROME (paginé) |
| GET | `/api/v1/all` | Tous les enregistrements (usage frontend SPA) |
| POST | `/api/v1/search` | Recherche par mots-clés |
| GET | `/api/v1/mapping/rome-to-naf/{code}` | Correspondances ROME → NAF |
| GET | `/api/v1/mapping/naf-to-rome/{code}` | Correspondances NAF → ROME |

### Exemples curl

```bash
# Santé de l'API
curl http://localhost:8000/health

# Données chargées (3 sources)
curl http://localhost:8000/metrics

# Liste des codes NAF (5 premiers)
curl "http://localhost:8000/api/v1/naf?limit=5"

# Correspondances NAF↔ROME
curl "http://localhost:8000/api/v1/matching?limit=5"

# Tous les enregistrements (732 NAF + 11337 ROME + 11126 matching)
curl "http://localhost:8000/api/v1/all" | python3 -m json.tool | head -20

# Recherche par mot-clé
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "informatique", "limit": 5}'

# Correspondance NAF → ROME
curl http://localhost:8000/api/v1/mapping/naf-to-rome/62.01Z
```

---

## Lancer les tests

### En local (venv Jour 2)

```bash
source ../jour02_fast_api/.venv/bin/activate

# Tous les tests
pytest tests/ -v

# Avec couverture de code
pytest tests/ -v --cov=app --cov-report=term-missing

# Rapport HTML
pytest tests/ --cov=app --cov-report=html
# Ouvrir htmlcov/index.html
```

### Dans Docker (approche CI/CD)

```bash
# Lance les tests dans le stage Docker isolé
docker build --target test -t naf-rome-test .

# Voir le résultat : exit code 0 = succès, 1 = échec
echo "Exit code: $?"
```

---

## Structure du projet

```
jour03_docker_ci_cd/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration via variables d'environnement
│   ├── main.py                # Point d'entrée FastAPI
│   ├── models.py              # Schémas Pydantic
│   ├── routers/
│   │   ├── health.py          # Routes /health et /metrics
│   │   └── mapping.py         # Routes /api/v1/...
│   └── services/
│       └── matcher.py         # Logique métier NAF/ROME (3 sources)
├── data/
│   ├── naf_codes_001_desc.csv             # 732 codes NAF
│   ├── rome.csv                           # 11 337 codes ROME
│   └── rome_with_naf__thenlper_gte-large.csv  # 11 126 correspondances NAF↔ROME
├── tests/
│   ├── conftest.py            # Fixtures pytest (3 CSV temporaires)
│   ├── test_health.py         # Tests endpoints de santé
│   └── test_mapping.py        # Tests endpoints de mapping (15 tests)
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline CI/CD GitHub Actions
├── .dockerignore
├── .pre-commit-config.yaml
├── docker-compose.yml         # API + Redis
├── Dockerfile                 # Multi-stage : builder → test → runtime
└── pyproject.toml
```

---

## Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `APP_DEBUG` | `false` | Mode debug |
| `APP_DATA_NAF_PATH` | `data/naf_codes_001_desc.csv` | Codes NAF |
| `APP_DATA_ROME_PATH` | `data/rome.csv` | Codes ROME |
| `APP_DATA_MATCHING_PATH` | `data/rome_with_naf__thenlper_gte-large.csv` | Correspondances |
| `APP_CORS_ORIGINS` | `["*"]` | Origines CORS autorisées |

---

## Objectifs pédagogiques

### A. Containerisation Docker
- [ ] Comprendre la structure d'un Dockerfile multi-stage (builder / test / runtime)
- [ ] Optimiser la taille de l'image (dépendances prod vs dev séparées)
- [ ] Utiliser un utilisateur non-root pour la sécurité
- [ ] Configurer le HEALTHCHECK Docker natif

### B. Tests dans Docker (CI/CD)
- [ ] Comprendre pourquoi les tests font partie du build (`--target test`)
- [ ] Écrire des fixtures pytest avec `tmp_path` (données isolées par test)
- [ ] Atteindre 70%+ de couverture de code
- [ ] Différencier tests unitaires, d'intégration et end-to-end

### C. Docker Compose
- [ ] Orchestrer plusieurs services (API + Redis)
- [ ] Gérer les dépendances entre services (`depends_on` + `condition: service_healthy`)
- [ ] Monter des volumes pour les données (`:ro` = lecture seule)
- [ ] Configurer les réseaux Docker isolés

### D. CI/CD avec GitHub Actions
- [ ] Créer un pipeline en 3 étapes : Lint → Test → Build/Push
- [ ] Publier une image Docker sur GitHub Container Registry (GHCR)
- [ ] Utiliser le cache Docker pour accélérer les builds
- [ ] Comprendre les triggers (`on: push`, `on: pull_request`)

---

## Exercices d'extension

### Niveau 1 — Amélioration des tests
1. Ajouter un test pour `GET /api/v1/all` qui vérifie que les 3 types sont présents
2. Ajouter un test de pagination sur `/api/v1/naf?limit=2&offset=1`
3. Atteindre 80%+ de couverture (`--cov-fail-under=80`)

### Niveau 2 — Cache Redis
1. Intégrer `redis-py` pour cacher les résultats de `keyword_search`
2. Ajouter un TTL de 5 minutes sur les entrées du cache
3. Exposer `DELETE /api/v1/cache` pour vider le cache manuellement

### Niveau 3 — Monitoring
1. Intégrer `prometheus-fastapi-instrumentator` pour les métriques réelles
2. Ajouter Grafana dans le docker-compose pour visualiser les métriques
3. Configurer une alerte sur le taux d'erreur > 1%

### Niveau 4 — Déploiement cloud
1. Déployer l'image sur Fly.io ou Render (gratuit)
2. Configurer les secrets (env vars) via l'interface cloud
3. Mettre en place un rolling deploy (zero downtime)

---

## Dépannage

### L'API ne démarre pas dans Docker
```bash
# Voir les logs détaillés
docker compose logs api

# Vérifier que les données sont montées
docker compose exec api ls -la /app/data/

# Tester l'image sans compose
docker run --rm -p 8000:8000 \
  -v $(pwd)/data:/app/data:ro \
  -e APP_DEBUG=true \
  naf-rome-api:local
```

### Les tests échouent dans Docker
```bash
# Lancer le stage test avec output détaillé
docker build --target test --progress=plain . 2>&1 | grep -A 30 "pytest"
```

### Erreur de permission Docker (Linux)
```bash
sudo usermod -aG docker $USER
# Se déconnecter/reconnecter
```

### Lancer les tests localement
```bash
# Avec le venv du Jour 2 (même dépendances)
source ../jour02_fast_api/.venv/bin/activate
pytest tests/ -v -s
```
