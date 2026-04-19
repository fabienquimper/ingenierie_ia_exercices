# TP 1.1 — FastAPI : Construction de l'API NAF-ROME

## Description

Ce TP fait évoluer l'application du Jour 1 en introduisant une **API REST FastAPI**
entre les données et le frontend. L'interface Vue.js est identique, mais elle ne lit
plus les CSV directement — elle interroge le backend Python.

**Durée estimée :** 1 journée (7h)

---

## Progression pédagogique : Jour 1 → Jour 2

| | Jour 1 — Frontend seul | Jour 2 — Frontend + API |
|---|---|---|
| **Données** | CSV chargés directement dans le navigateur | CSV chargés par le backend Python |
| **Architecture** | 1 couche (frontend) | 2 couches (frontend + API) |
| **Backend** | Aucun | FastAPI sur `localhost:8000` |
| **Recherche** | Filtrage JavaScript côté navigateur | Filtrage Python côté serveur |
| **Démarrage** | `./run.sh` (frontend seul) | `./run.sh` API + `./run.sh` frontend |
| **Scalabilité** | Limitée (tout en mémoire navigateur) | Meilleure (backend peut être optimisé) |

### Ce qui change dans le code

**Frontend (`src/services/`) :**
```
Jour 1 : csvService.ts  →  fetch('/naf_codes_001_desc.csv')
Jour 2 : apiService.ts  →  fetch('http://localhost:8000/api/v1/all')
```

**Traitement des données :**
```
Jour 1 : JavaScript dans le navigateur assigne le type (naf / rome / matching)
Jour 2 : Python dans le backend assigne le type au chargement des CSV
```

**Indicateur de connexion :**  
Le badge "API connectée / hors ligne" dans le header du Jour 2 est absent du Jour 1 —
c'est la conséquence directe d'avoir un service externe dont on dépend.

---

## Contexte métier

En France, deux référentiels coexistent pour décrire le monde du travail :

- **NAF (Nomenclature des Activités Françaises)** : classe les entreprises selon leur
  activité économique principale (ex: `62.01Z` = Programmation informatique)
- **ROME (Répertoire Opérationnel des Métiers et des Emplois)** : décrit les métiers
  exercés par les personnes (ex: `M1805` = Développement de logiciels)

L'enjeu : faire correspondre automatiquement ces deux référentiels pour faciliter
l'orientation professionnelle et le recrutement.

---

## Prérequis

- Python 3.12+
- Connaissance de base de Python
- Notions d'API REST (HTTP, JSON)

---

## Démarrage rapide

```bash
# 1. Aller dans le répertoire
cd jour02_fast_api

# 2. Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

# 3. Installer les dépendances
pip install -e "."

# 4. Lancer l'API
uvicorn app.main:app --reload --port 8000
```

Ou simplement :
```bash
bash run.sh
```

L'API est disponible sur : http://localhost:8000
Documentation interactive : http://localhost:8000/docs

---

## Explorer l'API

### Via le navigateur
Ouvrez http://localhost:8000/docs pour accéder à l'interface Swagger.
Vous pouvez tester tous les endpoints directement depuis le navigateur.

### Via curl

```bash
# Page d'accueil
curl http://localhost:8000/

# Santé de l'API
curl http://localhost:8000/health

# Lister les codes ROME (20 premiers)
curl "http://localhost:8000/api/v1/rome"

# Lister les codes NAF avec pagination
curl "http://localhost:8000/api/v1/naf?limit=5&offset=0"

# Détail d'un code ROME
curl http://localhost:8000/api/v1/rome/M1805

# Détail d'un code NAF
curl http://localhost:8000/api/v1/naf/62.01Z

# Recherche par mot-clé
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "programmation informatique", "limit": 5}'

# Correspondances NAF -> ROME
curl http://localhost:8000/api/v1/mapping/naf-to-rome/62.01Z

# Correspondances ROME -> NAF
curl http://localhost:8000/api/v1/mapping/rome-to-naf/M1805
```

---

## Structure du projet

```
jour02_fast_api/
├── app/
│   ├── config.py          # Configuration (pydantic-settings) — 3 chemins CSV
│   ├── main.py            # Application FastAPI + lifespan
│   ├── models.py          # Modèles Pydantic (request/response)
│   ├── routers/
│   │   ├── health.py      # GET /health, GET /metrics
│   │   └── mapping.py     # Tous les endpoints /api/v1/...
│   └── services/
│       └── matcher.py     # Chargement des 3 CSV + logique de recherche
├── data/
│   ├── naf_codes_001_desc.csv         # Codes NAF (type: naf)
│   ├── rome.csv                       # Codes ROME (type: rome)
│   ├── rome_with_naf__thenlper_gte-large.csv  # Correspondances (type: matching)
│   └── sample_naf_rome.csv            # Extrait minimal (tests)
├── frontend/
│   └── src/services/
│       ├── apiService.ts  # Jour 2 : appels vers l'API FastAPI
│       └── csvService.ts  # Jour 1 : chargement CSV direct (conservé pour référence)
├── pyproject.toml
├── run.sh
└── README.md
```

### Liste complète des endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Message de bienvenue |
| GET | `/health` | Santé + nombre d'enregistrements chargés |
| GET | `/metrics` | Métriques de monitoring |
| GET | `/api/v1/naf` | Liste paginée des codes NAF |
| GET | `/api/v1/rome` | Liste paginée des codes ROME |
| GET | `/api/v1/matching` | Liste paginée des correspondances NAF↔ROME |
| GET | `/api/v1/all` | **Tous les enregistrements** (usage frontend SPA) |
| GET | `/api/v1/naf/{code}` | Détail d'un code NAF + ROME associés |
| GET | `/api/v1/rome/{code}` | Détail d'un code ROME + NAF associés |
| GET | `/api/v1/mapping/naf-to-rome/{code}` | Correspondances NAF → ROME |
| GET | `/api/v1/mapping/rome-to-naf/{code}` | Correspondances ROME → NAF |
| POST | `/api/v1/search` | Recherche par mots-clés |

---

## Comprendre le code

### 1. `app/config.py` — Configuration
Utilise `pydantic-settings` pour lire la configuration depuis les variables d'environnement.
Le préfixe `APP_` permet de surcharger les chemins CSV :

```bash
APP_DATA_NAF_PATH=data/mon_naf.csv uvicorn app.main:app --reload
```

### 2. `app/models.py` — Schémas de données
Définit la forme des données entrantes et sortantes avec Pydantic v2.
FastAPI utilise ces modèles pour la validation et la documentation automatique.

### 3. `app/services/matcher.py` — Logique métier
C'est le coeur de l'application. La classe `NafRomeMatcher` :
- Charge le CSV en mémoire au démarrage
- Propose des méthodes de recherche et de correspondance
- Utilise le pattern Singleton pour n'avoir qu'une instance

### 4. `app/routers/` — Endpoints
Chaque fichier router regroupe les endpoints par thème.
Les routers sont enregistrés dans `main.py` avec `app.include_router()`.

---

## Objectifs pédagogiques

### A. Découverte de FastAPI
- [ ] Comprendre la structure d'une application FastAPI
- [ ] Utiliser le système de routeurs (`APIRouter`)
- [ ] Lire la documentation Swagger générée automatiquement
- [ ] Tester les endpoints avec Swagger UI ou curl

### B. Pydantic v2 — Validation des données
- [ ] Définir des modèles de requête et réponse
- [ ] Comprendre la validation automatique (types, longueurs, valeurs)
- [ ] Utiliser `Field` pour ajouter des contraintes et descriptions
- [ ] Comprendre les erreurs 422 (Unprocessable Entity)

### C. Architecture en couches
- [ ] Séparer la configuration, les routes, les modèles, les services
- [ ] Comprendre le pattern Repository/Service
- [ ] Utiliser le pattern Singleton pour les ressources partagées
- [ ] Gérer le cycle de vie de l'application (`lifespan`)

### D. Gestion des données
- [ ] Charger un CSV avec pandas
- [ ] Filtrer et rechercher dans un DataFrame
- [ ] Retourner des erreurs HTTP appropriées (404, 422)

---

## Exercices guidés

### Exercice 1 : Ajouter un endpoint de statistiques (Facile)

Créez l'endpoint `GET /api/v1/stats` qui retourne :
```json
{
  "total_records": 40,
  "naf_count": 20,
  "rome_count": 20,
  "unique_rome_codes": 20
}
```

**Indice :** Ajoutez une méthode `get_stats()` dans `matcher.py`, puis créez la route dans `mapping.py`.

### Exercice 2 : Filtrage par type (Facile)

Modifiez les endpoints `GET /api/v1/rome` et `GET /api/v1/naf` pour accepter
un paramètre de recherche `q` permettant de filtrer par nom.

```bash
curl "http://localhost:8000/api/v1/rome?q=informatique"
```

### Exercice 3 : Validation des codes NAF (Moyen)

Ajoutez une validation du format des codes NAF dans le endpoint `GET /api/v1/naf/{code_naf}`.
Le format attendu est : `XX.XXX` (2 chiffres, un point, 2 chiffres, une lettre majuscule).

**Indice :** Utilisez `re.match()` ou un validator Pydantic.

### Exercice 4 : Recherche avancée (Difficile)

Implémentez une recherche avec scoring TF-IDF simple :
1. Tokenisez les textes (name + desc) de chaque entrée
2. Calculez la fréquence de chaque terme dans le corpus
3. Utilisez ce score pour améliorer la pertinence des résultats

### Exercice 5 : Cache en mémoire (Difficile)

Implémentez un cache LRU simple pour les résultats de recherche :
1. Utilisez `functools.lru_cache` ou un dictionnaire manuel
2. Limitez le cache à 100 entrées
3. Ajoutez un endpoint `DELETE /cache` pour vider le cache

---

## Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Pydantic v2](https://docs.pydantic.dev/latest/)
- [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
- [Codes NAF - INSEE](https://www.insee.fr/fr/information/2120875)
- [Codes ROME - France Travail](https://www.francetravail.fr/employeur/vos-recrutements/le-rome-et-les-fiches-metiers.html)

---

## Pour aller plus loin (TP 1.2)

Le TP suivant (`jour03_docker_ci_cd/`) vous apprendra à :
- Containeriser cette API avec Docker
- Orchestrer les services avec docker-compose
- Mettre en place un pipeline CI/CD avec GitHub Actions
