# TP 1.1 — FastAPI : Construction de l'API NAF-ROME

## Description

Ce TP vous guide pour créer une API REST avec FastAPI permettant d'interroger
les correspondances entre codes NAF (activités économiques) et codes ROME (métiers).

**Durée estimée :** 1 journée (7h)

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
│   ├── __init__.py
│   ├── config.py          # Configuration (pydantic-settings)
│   ├── main.py            # Application FastAPI + lifespan
│   ├── models.py          # Modèles Pydantic (request/response)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py      # GET /health, GET /metrics
│   │   └── mapping.py     # Tous les endpoints /api/v1/...
│   └── services/
│       ├── __init__.py
│       └── matcher.py     # Logique de recherche et correspondance
├── data/
│   └── sample_naf_rome.csv  # Données d'exemple
├── pyproject.toml           # Dépendances et configuration
├── run.sh                   # Script de démarrage
└── README.md
```

---

## Comprendre le code

### 1. `app/config.py` — Configuration
Utilise `pydantic-settings` pour lire la configuration depuis les variables d'environnement.
Le préfixe `APP_` permet de distinguer les variables de l'application.

```python
# Exemple: surcharger le chemin des données
APP_DATA_PATH=data/mon_fichier.csv uvicorn app.main:app --reload
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
