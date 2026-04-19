# Jour 1 — UX/UI : Concevoir l'interface NAF-ROME

**Niveau :** Master IA · CreativeTech  
**Durée :** 1 journée (7h)  
**Objectif :** Avant de coder, on conçoit. Ce jour est entièrement consacré à la psychologie UX, aux personas, et au prototypage de l'interface.

---

## Le projet NAF ↔ ROME

L'application que vous allez construire sur 3 jours permet de faire correspondre des **codes NAF** (Nomenclature d'Activités Françaises, INSEE) et des **codes ROME** (Répertoire Opérationnel des Métiers et des Emplois, France Travail).

Elle expose **deux services distincts**, pour **deux types d'utilisateurs très différents** :

| | Service 1 — Matching structuré | Service 2 — Classification texte libre |
|---|---|---|
| **Persona** | Sophie, conseillère France Travail | Karim, chargé de veille économique (CCI) |
| **Input** | Code ROME, code NAF, ou mots-clés | Texte libre (offre d'emploi, description d'activité) |
| **Output** | Liste de codes correspondants filtrée | Codes NAF/ROME les plus probables + score de confiance |
| **Endpoint (jour 2)** | `GET /match?code_rome=M1805` | `POST /classify {"text": "..."}` |
| **UX clé** | Interface simple, max 5-7 résultats | Coller un texte → résultats immédiats avec scores |

> **Aujourd'hui vous ne codez pas.** Vous analysez, concevez, et prototypez.

---

## Les deux personas

### Sophie — 42 ans, Conseillère France Travail

> *"Je passe des heures dans des tableaux Excel pour trouver quels métiers correspondent à l'activité d'une entreprise. C'est épuisant."*

- **Poste :** Conseillère en insertion professionnelle, agence France Travail de Lyon
- **Usage :** Accompagne des demandeurs d'emploi vers des entreprises qui recrutent. Doit croiser les codes NAF des entreprises avec les codes ROME des candidats.
- **Niveau technique :** À l'aise avec les outils bureautiques, peu habituée aux applications web avancées
- **Frustration principale :** Les référentiels NAF et ROME sont complexes, les tables de correspondance Excel ne sont pas intuitives
- **Besoin UX :** Interface simple, résultats filtrés (Loi de Miller : 5-7 max), langage métier compréhensible sans connaître les codes
- **Scénario type :** Cherche les métiers ROME compatibles avec une entreprise de code NAF `62.01Z` pour orienter un candidat développeur

### Karim — 35 ans, Chargé de veille économique (CCI)

> *"Je reçois des dizaines d'offres d'emploi et de descriptions d'entreprises. Je dois les classer manuellement en codes NAF/ROME. C'est du copier-coller sans fin."*

- **Poste :** Chargé de veille et d'analyse économique, Chambre de Commerce et d'Industrie
- **Usage :** Reçoit des textes bruts (offres d'emploi, fiches entreprises) et doit les classer en codes NAF/ROME pour ses rapports de veille
- **Niveau technique :** Habitué aux tableurs et à l'analyse de données, pas de compétences en API ou en code
- **Frustration principale :** Classement manuel long et sujet à erreurs, pas d'outil adapté à son workflow
- **Besoin UX :** Coller un texte → obtenir immédiatement les codes probables avec un **score de confiance** et une **justification**
- **Scénario type :** Colle une offre d'emploi → obtient `ROME M1805 (90%)` + `NAF 62.01Z (85%)` + explication en langage naturel

> *Bonus — contexte étendu :* Karim a un collègue développeur qui aimerait exposer
> ce même service sous forme d'API pour traiter des offres en masse automatiquement.
> Karim est en quelque sorte le "testeur métier" de ce que le dev voudrait industrialiser —
> un bon pont pour expliquer le passage jour 1 (UX) → jour 2 (API) → jour 3 (Docker).

---

## L'application de référence (Service 1 — Sophie)

Le dossier `03frontend/` contient une **implémentation de référence fonctionnelle** du Service 1.

```bash
cd 03frontend
./run.sh
# → http://localhost:5173
```

> **Ce frontend est un exemple, pas le livrable.** Il illustre le Service 1 (Sophie).  
> Votre travail aujourd'hui : **l'analyser, le critiquer, et concevoir ce qui manque** — notamment le Service 2 (Karim).

Ce que ce frontend fait :
- Charge 3 CSV (NAF, ROME, correspondances) directement dans le navigateur
- Recherche par mots-clés ou code
- Filtre par type (NAF / ROME / Matching)
- Tableau de résultats paginé, triable, exportable CSV
- Lignes expansibles pour voir la description complète
- Accessible au clavier (RGAA niveau A)

Ce qu'il ne fait **pas** (à concevoir aujourd'hui) :
- Interface de classification texte libre (Service 2 / Karim)
- Score de confiance visible
- Mode vocal / Whisper (bonus)
- Explication des résultats en langage naturel

---

## Psychologie cognitive appliquée à l'UX

Avant de concevoir, comprenez ces lois. Elles guident chaque décision de design.

| Loi | Principe | Application dans notre app |
|---|---|---|
| **Loi de Miller** | L'humain traite 7 ± 2 éléments en mémoire de travail | Max 5-7 résultats par page pour Sophie |
| **Loi de Hick** | Plus il y a de choix, plus la décision est longue | Filtres réduits au minimum, pas de menus complexes |
| **Loi de Fitts** | Le temps pour atteindre une cible dépend de sa taille et distance | Boutons d'action grands et proches du contenu |
| **Gestalt — Proximité** | Des éléments proches semblent liés | Code NAF + libellé + score groupés visuellement |
| **Gestalt — Similarité** | Des éléments similaires visuellement semblent appartenir au même groupe | Badges couleur cohérents : bleu NAF, violet ROME, vert Matching |
| **Effet de primauté/récence** | On retient mieux le début et la fin d'une liste | Résultats les plus pertinents en premier, action d'export en dernier |

---

## Outils de prototypage

### Étape 1 — Wireframe basse fidélité (Excalidraw)

Un wireframe de référence est fourni : `01excalidraw/wireframe_naf_rome.excalidraw`

- Ouvrir en ligne : [excalidraw.com](https://excalidraw.com) → `File → Open`
- Extension VS Code : [Excalidraw Editor](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor)

Ce wireframe couvre l'interface Sophie (Service 1). Vous devrez créer le wireframe de l'interface Karim (Service 2).

### Étape 2 — Prototype haute fidélité (Penpot)

**Penpot** est recommandé (open source, gratuit, collaborative) :
- En ligne : [penpot.app](https://penpot.app)
- En local (Docker) : `docker compose -p penpot -f 02penpot/docker-compose.yaml up -d` → [localhost:9001](http://localhost:9001)

**Figma** est aussi accepté : [figma.com](https://www.figma.com) (plan gratuit suffisant)

---

## Livrables attendus

### 1. Analyse de l'existant — Service 1 (45 min)

Lancez `03frontend` et analysez-le en tant que **Sophie** :
- Quelles lois cognitives sont respectées ? Lesquelles sont violées ?
- Identifiez 3 points forts et 3 améliorations prioritaires
- Vérifiez 5 critères RGAA (voir checklist ci-dessous)

### 2. Personas documentés (30 min)

Complétez les fiches Sophie et Karim avec :
- Une photo (Unsplash, libre de droits)
- Leurs objectifs, frustrations, contexte d'usage
- Leur parcours type (user journey en 5 étapes)

### 3. User Stories (30 min)

Rédigez **6 user stories minimum** (3 par persona) au format :
> En tant que **[persona]**, je veux **[action]** afin de **[bénéfice]**.

Exemples :
- En tant que **Sophie**, je veux **saisir un code NAF et voir les 5 métiers ROME les plus proches** afin de **gagner du temps dans l'orientation**.
- En tant que **Karim**, je veux **coller une offre d'emploi et obtenir un code ROME avec un score** afin de **automatiser mon classement**.

### 4. Wireframes (2h)

Créez en Excalidraw les maquettes basse fidélité de :

**Interface Sophie (Service 1) — amélioration de l'existant :**
- Page de recherche (barre + filtres)
- Page de résultats (5-7 résultats max, badges couleur)
- Détail d'une correspondance

**Interface Karim (Service 2) — à concevoir :**
- Zone de saisie de texte libre (grande, visible, accueillante)
- Résultats avec scores de confiance (ex: `ROME M1805 — 90%`)
- Justification en langage naturel

**Bonus — Mode vocal Whisper :**
- Bouton microphone
- Feedback visuel d'enregistrement
- Transition vers les résultats

### 5. Prototype interactif (2h)

Dans Penpot ou Figma, rendez votre prototype navigable :
- Barre de recherche → résultats
- Résultat → détail
- Zone texte Karim → résultats avec scores
- Bouton retour fonctionnel
- Couleurs et typographie définies (design system minimal)

---

## Checklist RGAA — dès le prototypage

Ces critères doivent être pensés **dans la maquette**, pas ajoutés après le code.

| # | Critère | À vérifier dans Penpot |
|---|---|---|
| 1 | Contraste texte/fond ≥ 4.5:1 (niveau AA) | Utiliser le contrast checker de Penpot |
| 2 | Labels visibles sur tous les champs de formulaire | Pas de placeholder seul comme label |
| 3 | Navigation clavier logique (ordre Tab cohérent) | Annoter l'ordre de focus dans la maquette |
| 4 | Messages d'erreur textuels (pas seulement couleur rouge) | Ajouter un texte d'erreur sous le champ |
| 5 | Texte alternatif sur les icônes porteuses de sens | Annoter `aria-label` dans la maquette |
| 6 | Taille des zones cliquables ≥ 44×44px | Vérifier les boutons et liens dans Penpot |
| 7 | Hiérarchie de titres logique (h1 → h2 → h3) | Annoter la sémantique HTML dans la maquette |
| 8 | Indicateur de focus visible | Prévoir un style `:focus` visible dans le design |
| 9 | Pas d'information transmise par la couleur seule | Les badges NAF/ROME ont du texte ET une couleur |
| 10 | Langue de la page déclarée (`lang="fr"`) | Note dans les specs techniques du prototype |

---

## Ateliers pratiques

Ces ateliers sont **chronométrés et obligatoires** — ils se font avant d'ouvrir Penpot.
Le meilleur UX se conçoit d'abord sur papier.

### Atelier 0 — Crazy 8s (20 min · solo puis binôme)

> Objectif : générer rapidement des idées sans se censurer.

1. Prenez une feuille A4, pliez-la en 8 cases
2. Réglez un minuteur sur **8 minutes**
3. Dessinez **8 esquisses différentes** de la page principale de l'interface Karim (Service 2)
   — une idée par case, peu importe la qualité du dessin
4. En binôme : présentez vos 8 idées en 2 minutes chacun
5. Chacun place **2 gommettes** (ou croix) sur les idées de l'autre qu'il préfère
6. Les idées avec le plus de votes deviennent la base de votre wireframe

**Photographiez votre feuille Crazy 8s — c'est un livrable.**

---

### Atelier 1 — Think-Aloud avec un binôme (20 min)

> Objectif : observer un vrai comportement utilisateur plutôt qu'imaginer.

**Rôles :** A = facilitateur, B = utilisateur (joue le rôle de Sophie ou Karim)

> *Suggestion :* Si vous avez accès à Claude ou ChatGPT, vous pouvez demander au LLM
> de jouer le rôle de Karim pendant le test — décrivez-lui le persona et la tâche,
> puis posez-lui des questions comme "qu'est-ce que tu ferais face à cet écran ?".
> C'est une façon rapide de simuler un utilisateur quand on n'a pas de vrai testeur disponible.

1. **A** donne la tâche à voix haute à **B** :
   > *"Tu es Sophie, conseillère France Travail. Un candidat développeur est en face de toi.
   > Son entreprise cible a le code NAF 62.01Z. Trouve les métiers ROME correspondants."*
2. **B** verbalise TOUT ce qu'il pense en naviguant sur `localhost:5173` ("je cherche...", "je ne comprends pas...", "je m'attends à...")
3. **A** ne répond PAS, note sur papier : les hésitations, les erreurs, les commentaires spontanés
4. Après 10 minutes : échangez les rôles (B devient facilitateur, A joue Karim avec le Service 2)

**Notez au moins 3 blocages observés — ils deviendront vos "How Might We".**

---

### Atelier 2 — Heuristiques de Nielsen (20 min · binôme)

> Objectif : structurer la critique avec un framework professionnel.

Les 10 heuristiques de Nielsen sont le standard mondial d'évaluation d'interface.
Appliquez-les à `03frontend` en complétant ce tableau :

| # | Heuristique | Conforme ? | Observation sur notre app |
|---|---|---|---|
| 1 | Visibilité du statut système | ✅ / ⚠️ / ❌ | |
| 2 | Correspondance système/monde réel | ✅ / ⚠️ / ❌ | |
| 3 | Contrôle et liberté | ✅ / ⚠️ / ❌ | |
| 4 | Cohérence et standards | ✅ / ⚠️ / ❌ | |
| 5 | Prévention des erreurs | ✅ / ⚠️ / ❌ | |
| 6 | Reconnaissance plutôt que rappel | ✅ / ⚠️ / ❌ | |
| 7 | Flexibilité et efficacité | ✅ / ⚠️ / ❌ | |
| 8 | Esthétique et minimalisme | ✅ / ⚠️ / ❌ | |
| 9 | Aide à la récupération d'erreur | ✅ / ⚠️ / ❌ | |
| 10 | Aide et documentation | ✅ / ⚠️ / ❌ | |

---

### Atelier 3 — How Might We (15 min · solo → groupe)

> Objectif : transformer les blocages du Think-Aloud en opportunités de design.

À partir des 3+ blocages observés en Atelier 1, rédigez des questions "Comment pourrions-nous..." :

Format : **"Comment pourrions-nous [verbe d'action] pour que [persona] puisse [objectif] ?"**

Exemples à partir de blocages réels :
- Blocage : *"Sophie ne trouve pas les correspondances NAF↔ROME"*
  → HMW : *"Comment pourrions-nous rendre le concept de 'correspondance' immédiatement compréhensible sans formation ?"*
- Blocage : *"Karim ne sait pas où coller son texte"*
  → HMW : *"Comment pourrions-nous faire de la zone de saisie l'élément le plus visible de la page ?"*

Chaque étudiant rédige **3 HMW solo**, puis le groupe vote les 2 meilleurs pour guider le wireframe.

---

### Atelier 4 — Design assisté par IA *(Optionnel — bonus)*

> ⚠️ **Optionnel** : cet atelier utilise un LLM (Claude, ChatGPT). Il nécessite un accès
> à un compte (gratuit sur claude.ai ou chatgpt.com). Environ 5-10 échanges par atelier.
>
> Si vous n'avez pas d'accès, lisez la narration ci-dessous pour comprendre l'approche.

Le fichier [`METAPROMPT_design_naf_rome.md`](METAPROMPT_design_naf_rome.md) contient :
- Un **contexte système** à coller dans Claude (décrit Sophie, Karim, les contraintes RGAA)
- **8 commandes** prêtes à l'emploi : critique de maquette, spec de composant, audit RGAA, HMW...
- Une **narration complète** d'une session type (comment Amina l'a utilisé)

**En 20 minutes avec ce méta-prompt, vous pouvez :**
1. Faire auditer votre wireframe Crazy 8s par Claude (Commande 1)
2. Obtenir la spec HTML/aria complète d'un composant (Commande 3)
3. Générer 8 HMW à partir de vos observations (Commande 5)

---

## Planning suggéré

Les durées sont indicatives — la journée est volontairement flexible.
Certains ateliers peuvent déborder, c'est normal et pédagogique.

### Bloc 1 — Cadrage et théorie (~1h30)

| Durée | Activité | Format |
|---|---|---|
| ~30 min | Introduction : projet NAF/ROME, personas Sophie & Karim, 2 services | Collectif |
| ~45 min | Théorie UX : Miller, Hick, Fitts, Gestalt, Nielsen — appliqués au projet | Collectif |
| ~15 min | Prise en main de `03frontend` (lancer l'app, explorer librement) | Solo |

### Bloc 2 — Ateliers pratiques (~1h30)

| Durée | Activité | Format |
|---|---|---|
| ~20 min | **Atelier 1 — Think-Aloud** : tester `03frontend` en jouant Sophie/Karim | Binôme |
| ~20 min | **Atelier 2 — Nielsen** : audit des 10 heuristiques sur `03frontend` | Binôme |
| ~15 min | **Atelier 3 — How Might We** : transformer les blocages en opportunités | Solo → vote groupe |
| ~20 min | **Atelier 0 — Crazy 8s** : 8 esquisses papier du Service 2 Karim | Solo → binôme |

### Bloc 3 — Conception (~2h)

| Durée | Activité | Format |
|---|---|---|
| ~30 min | Personas documentés + User Stories (6 minimum) | Solo ou binôme |
| ~1h30 | Wireframes Excalidraw : Service 1 amélioré + Service 2 Karim | Solo ou binôme |

### Bloc 4 — Prototypage (~1h30)

| Durée | Activité | Format |
|---|---|---|
| ~1h15 | Prototype haute fidélité Penpot/Figma (couleurs, typo, composants, liens) | Solo ou binôme |
| ~15 min | Checklist RGAA sur le prototype (10 critères) | Solo |

### Bloc 5 — Clôture (~30 min)

| Durée | Activité | Format |
|---|---|---|
| ~20 min | Présentation inter-groupes + feedback collectif | Collectif |
| ~10 min | **Atelier 4 *(optionnel)*** — Design assisté par IA (méta-prompt Claude) | Solo |

---

> **RGAA — note pour le jour 4 (autonomie)**
>
> La checklist RGAA du Bloc 4 est une **introduction** — 10 critères fondamentaux.
> Le RGAA 4.1 complet (106 critères, 13 thèmes) sera approfondi en journée d'autonomie :
> audit WAVE sur 5 sites réels, heuristiques par thème, déclaration d'accessibilité.
> Ce que vous faites aujourd'hui dans la maquette est le bon réflexe : intégrer
> l'accessibilité **dès la conception**, pas en post-correction du code.

---

## Lien avec les jours suivants

| Ce que vous concevez aujourd'hui | Ce que ça implique pour le code |
|---|---|
| Barre de recherche Service 1 | `GET /api/v1/search?query=...` (jour 2) |
| Filtres NAF / ROME / Matching | `GET /api/v1/naf`, `/rome`, `/matching` (jour 2) |
| Zone texte Service 2 Karim | `POST /api/v1/classify {"text": "..."}` (jour 2+) |
| Traitement en masse (collègue dev de Karim) | Même endpoint appelé 500× en boucle via API (jour 3) |
| Score de confiance affiché | Champ `score` dans le JSON de réponse |
| Bouton export CSV | Logique côté frontend (jour 2) |

> **Le prototype Penpot que vous créez aujourd'hui est le cahier des charges visuel de l'API que vous allez construire demain.**

---

## Ressources

| Ressource | URL |
|---|---|
| Excalidraw (wireframe) | https://excalidraw.com |
| Penpot (prototype open source) | https://penpot.app |
| Figma (alternative) | https://figma.com |
| DSFR — Design Système de l'État | https://www.systeme-de-design.gouv.fr/ |
| WebAIM Contrast Checker | https://webaim.org/resources/contrastchecker/ |
| Heroicons (icônes open source) | https://heroicons.com |
| Loi de Miller (Wikipedia) | https://fr.wikipedia.org/wiki/Nombre_magique_(psychologie) |
| RGAA 4.1 officiel | https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/ |
| Unsplash (photos libres) | https://unsplash.com |
| **Méta-prompt Design IA** *(optionnel)* | `METAPROMPT_design_naf_rome.md` |
