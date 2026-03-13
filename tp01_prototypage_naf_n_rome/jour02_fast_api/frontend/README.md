# Interface NAF ↔ ROME — Jour 2 (source API FastAPI)

Même interface que le Jour 1, mais les données proviennent maintenant de **l'API FastAPI**
qui tourne en local. Cela illustre la séparation frontend / backend.

---

## Prérequis

| Outil | Version minimale | Vérification |
|-------|-----------------|--------------|
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Python | 3.12+ | `python3 --version` |
| API démarrée | — | voir ci-dessous |

---

## Démarrage (2 terminaux)

### Terminal 1 — Lancer l'API FastAPI

```bash
cd jour02_fast_api
./run.sh
# → API disponible sur http://localhost:8000
# → Swagger UI : http://localhost:8000/docs
```

### Terminal 2 — Lancer le frontend

```bash
cd jour02_fast_api/frontend
./run.sh
# → Interface disponible sur http://localhost:5174
```

> Le header affiche une **pastille verte** si l'API répond, rouge sinon.

---

## Arrêt

```bash
# Arrêter le frontend
cd jour02_fast_api/frontend && ./stop.sh

# Arrêter l'API
cd jour02_fast_api && ./stop.sh

# Ou simplement Ctrl+C dans chaque terminal
```

---

## Commandes npm détaillées

```bash
# Installer les dépendances
npm install

# Démarrer le serveur de développement (hot-reload + proxy vers :8000)
npm run dev

# Compiler pour la production
npm run build

# Prévisualiser le build de production
npm run preview
```

---

## Configuration

Copiez `.env.example` en `.env` pour changer l'URL de l'API :

```bash
cp .env.example .env
```

```env
# .env
VITE_API_URL=http://localhost:8000
```

> En production, remplacez par l'URL de votre serveur déployé.

---

## Structure du projet

```
frontend/
├── src/
│   ├── App.vue                   ← identique au Jour 1 (badge "Jour 2" + indicateur API)
│   ├── services/
│   │   ├── csvService.ts         ← réutilisé pour recherche locale + export CSV
│   │   └── apiService.ts         ← appels FastAPI (loadData, searchApi)
│   └── components/               ← identiques au Jour 1
│       ├── SearchBar.vue
│       ├── ResultsTable.vue
│       └── StatsBar.vue
├── .env.example                  ← template de configuration
├── run.sh                        ← démarrage en une commande
├── stop.sh                       ← arrêt par port
└── vite.config.ts                ← proxy /api → localhost:8000
```

---

## Endpoints API utilisés

| Endpoint | Méthode | Usage |
|----------|---------|-------|
| `/api/v1/naf?limit=100` | GET | Chargement des codes NAF |
| `/api/v1/rome?limit=100` | GET | Chargement des codes ROME |
| `/api/v1/search` | POST | Recherche par mots-clés (serveur) |
| `/health` | GET | Vérification que l'API répond |

Documentation interactive : **http://localhost:8000/docs**

---

## Proxy Vite (pas de problème CORS)

En développement, Vite redirige automatiquement :

```
http://localhost:5174/api/...  →  http://localhost:8000/api/...
http://localhost:5174/health   →  http://localhost:8000/health
```

Pas besoin de configurer CORS pour le développement local.

---

## Différence avec le Jour 1

| | Jour 1 | Jour 2 |
|---|--------|--------|
| Source de données | CSV local (navigateur) | API FastAPI (réseau) |
| Backend requis | Non | Oui (`./run.sh` dans `jour02_fast_api/`) |
| Port frontend | 5173 | 5174 |
| Indicateur API | — | Pastille verte/rouge dans le header |
| Recherche | Locale (client) | Locale + endpoint `/search` disponible |
