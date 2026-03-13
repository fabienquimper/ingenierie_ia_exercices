# Jour 1 — Notebooks NAF/ROME (données sources)

Ce dossier contient les notebooks Jupyter du projet
[NAFnROME](https://github.com/fabienquimper/NAFnROME) qui génèrent les données
utilisées dans tous les TPs suivants.

> Le dossier `NAFnROME/` n'est **pas versionné ici** — c'est un dépôt git
> indépendant à cloner séparément (voir ci-dessous).

---

## Contexte

Les notebooks téléchargent les référentiels officiels (INSEE, France Travail),
les traitent, et produisent des fichiers CSV prêts à l'emploi :

| Fichier CSV généré | Contenu |
|--------------------|---------|
| `naf_codes_001_desc.csv` | ~730 codes NAF avec descriptions longues (INSEE) |
| `rome_with_naf_all-MiniLM-L6-v2.csv` | 1 584 métiers ROME avec le code NAF le plus proche |
| `fusion_naf_rome_001_allMiniLM_L6_v2.csv` | Fusion complète NAF + ROME — **11 858 enregistrements** |

---

## Prérequis

| Outil | Version | Vérification |
|-------|---------|--------------|
| Python | 3.10+ | `python3 --version` |
| pip | récent | `pip --version` |
| Accès Internet | — | téléchargements INSEE + modèles ML |
| RAM | 4 Go min | le modèle `all-MiniLM-L6-v2` (~80 Mo) |

---

## Installation

### 1. Cloner le dépôt NAFnROME

```bash
cd jour01_naf_rome
git clone https://github.com/fabienquimper/NAFnROME
cd NAFnROME
```

### 2. Créer l'environnement virtuel

```bash
# Linux / macOS / WSL
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

> Premier lancement : le modèle `sentence-transformers/all-MiniLM-L6-v2`
> (~80 Mo) sera téléchargé automatiquement depuis HuggingFace.

### 4. Lancer Jupyter

```bash
jupyter lab
# ou
jupyter notebook
```

---

## Pipeline des notebooks — exécuter dans l'ordre

```
01 → 02 → 03 → 04 → 05   (génération des données)
              ↓
             06           (exploration / recherche)
```

### `01_BUILD__rome_csv.ipynb` — Référentiel ROME
- Télécharge le ZIP officiel ROME depuis data.gouv.fr
- Parse le XML (`unix_fiche_emploi_metier_v460_iso8859-15.xml`)
- **Produit :** `rome.csv` — 1 584 fiches métier (code, nom, description, appellations)

### `02_BUILD__naf_codes_001_csv.ipynb` — Codes NAF
- Télécharge le fichier XLS NAF depuis l'INSEE
- Valide les codes (format `XX.XXZ`)
- **Produit :** `naf_codes_001.csv` — ~730 codes NAF + intitulés

### `03_EXTRACT_naf_codes_001_desc_csv__from_pdf.ipynb` — Descriptions NAF
- Télécharge le PDF officiel INSEE "Nomenclatures NAF et CPF"
- Extrait les descriptions longues via `pdfplumber` + regex
- **Produit :** `naf_codes_001_desc.csv` — codes NAF enrichis de descriptions complètes

### `04_GEN__rome_with_naf_csv.ipynb` — Similarité sémantique ROME → NAF ⚠️ lent
- Charge le modèle `sentence-transformers/all-MiniLM-L6-v2`
- Calcule la similarité cosinus entre chaque description ROME et chaque code NAF
- **Produit :** `rome_with_naf_all-MiniLM-L6-v2.csv`

> **Note :** Ce notebook peut prendre **5 à 15 minutes** selon votre machine.
> Les associations sont indicatives (similarité textuelle, pas sémantique parfaite).

### `05_BUILD__fusion_naf_rome_001_csv.ipynb` — Fusion finale
- Concatène les données NAF enrichies et ROME avec mappings
- **Produit :** `fusion_naf_rome_001_allMiniLM_L6_v2.csv` — **11 858 enregistrements**

### `06_FIND_best_NAF_codes_from_keywords_.ipynb` — Recherche interactive
- Exploration libre : recherche par mots-clés ou embeddings
- Exemples fournis : `"yoga"`, `"traiteur"`, `"fast food"`, `"professeur"`
- Utilise ChromaDB comme base vectorielle locale
- **Pas de CSV produit** — notebook d'exploration uniquement

---

## Utiliser les données dans les TPs

Une fois les notebooks `01 → 05` exécutés, copiez le CSV final vers les autres TPs :

```bash
# Vers l'API FastAPI (Jour 2)
cp fusion_naf_rome_001_allMiniLM_L6_v2.csv \
   ../../jour02_fast_api/data/sample_naf_rome.csv

# Vers Docker (Jour 3)
cp fusion_naf_rome_001_allMiniLM_L6_v2.csv \
   ../../jour03_docker_ci_cd/data/sample_naf_rome.csv

# Vers le frontend (Jour 1 UX)
cp fusion_naf_rome_001_allMiniLM_L6_v2.csv \
   ../../jour01_ux_ui/frontend/public/data/sample_naf_rome.csv
```

> Le fichier `sample_naf_rome.csv` fourni par défaut contient **40 enregistrements**
> de démonstration. Le fichier complet en contient **11 858**.

---

## Limitations connues

- Les associations ROME → NAF sont **indicatives** : elles reposent sur la
  similarité textuelle et peuvent contenir des erreurs
- Les descriptions NAF extraites du PDF peuvent avoir du bruit résiduel
- Le modèle `all-MiniLM-L6-v2` est léger mais pas spécialisé en français

---

## Structure après clonage et exécution

```
jour01_naf_rome/
├── .gitignore                          ← ignore NAFnROME/ et les CSV générés
├── README.md                           ← ce fichier
└── NAFnROME/                           ← dépôt cloné (non versionné ici)
    ├── 01_BUILD__rome_csv.ipynb
    ├── 02_BUILD__naf_codes_001_csv.ipynb
    ├── 03_EXTRACT_naf_codes_001_desc_csv__from_pdf.ipynb
    ├── 04_GEN__rome_with_naf_csv.ipynb       ← ⚠️ lent (5-15 min)
    ├── 05_BUILD__fusion_naf_rome_001_csv.ipynb
    ├── 06_FIND_best_NAF_codes_from_keywords_.ipynb  ← exploration
    ├── naf_codes_001_desc.csv                ← généré par 03
    ├── rome_with_naf_all-MiniLM-L6-v2.csv   ← généré par 04
    └── fusion_naf_rome_001_allMiniLM_L6_v2.csv  ← ⭐ fichier principal
```
