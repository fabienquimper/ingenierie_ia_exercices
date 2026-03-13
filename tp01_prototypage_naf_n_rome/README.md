# TP Bloc 4 — Déployer une solution IA
### NAF ↔ ROME · Master IA · CreativeTech · Avril–Juillet 2026

Dépôt de travaux pratiques basé sur le projet
[NAFnROME](https://github.com/fabienquimper/NAFnROME) —
correspondance sémantique entre codes d'activité (NAF) et codes métier (ROME).

---

## Vue d'ensemble

```
tp01_prototypage_naf_n_rome/
├── jour01_ux_ui/          TP 1.0 — UX/UI + Interface CSV (Vue 3)
├── jour02_fast_api/       TP 1.1 — API FastAPI + Interface API (Vue 3)
├── jour03_docker_ci_cd/   TP 1.2 — Docker & CI/CD GitHub Actions
├── jour04_test/           TP 1.3 — Tests & Qualité (Pytest, Coverage)
└── jour05_prototypage/    Jour 5  — Autonomie & Débriefing
```

---

## Démarrage rapide par jour

### Jour 1 — Interface CSV (sans backend)

```bash
cd jour01_ux_ui/frontend
./run.sh
# → http://localhost:5173
```

### Jour 2 — API FastAPI + Interface

**Terminal 1 — API :**
```bash
cd jour02_fast_api
./run.sh
# → http://localhost:8000
# → Swagger : http://localhost:8000/docs
```

**Terminal 2 — Frontend :**
```bash
cd jour02_fast_api/frontend
./run.sh
# → http://localhost:5174
```

### Jour 3 — Docker

```bash
cd jour03_docker_ci_cd
docker compose up --build
# → http://localhost:8000
```

---

## Scripts disponibles

| Dossier | Script | Action |
|---------|--------|--------|
| `jour01_ux_ui/frontend/` | `./run.sh` | Démarre le frontend Jour 1 (port 5173) |
| `jour01_ux_ui/frontend/` | `./stop.sh` | Arrête le frontend Jour 1 |
| `jour02_fast_api/` | `./run.sh` | Démarre l'API FastAPI (port 8000) |
| `jour02_fast_api/` | `./stop.sh` | Arrête l'API FastAPI |
| `jour02_fast_api/frontend/` | `./run.sh` | Démarre le frontend Jour 2 (port 5174) |
| `jour02_fast_api/frontend/` | `./stop.sh` | Arrête le frontend Jour 2 |

---

## Prérequis globaux

| Outil | Version | Usage |
|-------|---------|-------|
| Python | 3.12+ | API FastAPI |
| Node.js | 18+ | Frontend Vue 3 |
| npm | 9+ | Gestionnaire de paquets JS |
| Docker | 24+ | TP 1.2 |
| Git | 2.40+ | Versionning & CI/CD |

Vérification rapide :
```bash
python3 --version && node --version && npm --version && docker --version
```

---

## Architecture de la Phase 1

```
Navigateur (Vue 3 + TypeScript)
        │
        │  Jour 1 : fetch CSV local
        │  Jour 2 : HTTP → FastAPI
        ▼
   FastAPI (Python 3.12)
        │  uvicorn
        │  pandas + structlog
        ▼
   data/sample_naf_rome.csv
   (ou données complètes générées par les notebooks)
```

---

## Données

Le fichier `data/sample_naf_rome.csv` contient 40 enregistrements de démonstration.

Pour utiliser les **données complètes** (~11 858 enregistrements) :
1. Clonez [NAFnROME](https://github.com/fabienquimper/NAFnROME)
2. Exécutez les notebooks `01` à `05` dans l'ordre
3. Copiez `fusion_naf_rome_001_allMiniLM_L6_v2.csv` dans le dossier `data/`
4. Mettez à jour `APP_DATA_PATH` dans votre `.env`

---

## Liens utiles

| Ressource | URL |
|-----------|-----|
| Repository NAFnROME | https://github.com/fabienquimper/NAFnROME |
| Codes ROME (France Travail) | https://www.francetravail.fr/employeur/vos-recrutements/le-rome-et-les-fiches-metiers.html |
| Codes NAF (INSEE) | https://www.insee.fr/fr/information/2120875 |
| FastAPI docs | https://fastapi.tiangolo.com |
| Vue 3 docs | https://vuejs.org |
