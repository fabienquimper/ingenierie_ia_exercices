# Évaluation — Jour 1 : UX/UI & Prototypage NAF-ROME

**Niveau :** Master IA · CreativeTech  
**Durée estimée :** 3h30 à 4h  
**Rendu :** un document réponse (PDF ou Markdown) + captures d'écran annotées + fichiers Penpot/Figma exportés

---

## Contexte

Vous concevez l'interface d'une application de matching NAF ↔ ROME pour **deux utilisateurs aux besoins très différents** :

- **Sophie**, 42 ans, conseillère France Travail — interface de recherche structurée
- **Karim**, 35 ans, chargé de veille économique (CCI) — interface de classification texte libre

Une **application de référence fonctionnelle** (Service 1 / Sophie) est disponible dans `03frontend/`. Lancez-la avant de commencer :

```bash
cd 03frontend && ./run.sh
# → http://localhost:5173
```

---

## Partie 0 — Livrables des ateliers pratiques

> Ces livrables sont produits **pendant** la journée, avant d'ouvrir Penpot.
> Ils sont obligatoires sauf mention *(optionnel)*.

### A1 — Crazy 8s (Atelier 0)

**Livrable :** Photo de votre feuille A4 pliée en 8 cases avec vos esquisses papier.

**Questions :**

A1a. Parmi vos 8 esquisses, laquelle a reçu le plus de gommettes de votre binôme ? Décrivez-la en 3 phrases et expliquez pourquoi elle a été choisie.

A1b. Quelle esquisse vous semblait la plus créative mais n'a pas été retenue ? Pourquoi pensez-vous qu'elle n'a pas convaincu ?

---

### A2 — Think-Aloud (Atelier 1)

**Livrable :** Notes de facilitation : liste des hésitations, erreurs et commentaires observés.

**Questions :**

A2a. Listez les **3 blocages principaux** observés pendant le test (celui qui jouait Sophie ou Karim). Pour chacun : à quelle étape s'est-il produit, qu'a dit l'utilisateur, quelle est votre interprétation UX ?

A2b. Y a-t-il eu un moment où l'utilisateur a fait quelque chose d'**inattendu** — une action que vous n'aviez pas anticipée ? Décrivez-la.

---

### A3 — Heuristiques de Nielsen (Atelier 2)

**Livrable :** Tableau des 10 heuristiques complété (voir README).

**Questions :**

A3a. Quelle heuristique est la **plus violée** dans `03frontend` ? Justifiez avec un exemple précis d'interaction.

A3b. Quelle heuristique est la **mieux respectée** ? Donnez un exemple qui illustre ce point fort.

---

### A4 — How Might We (Atelier 3)

**Livrable :** Vos 3 formulations HMW + les 2 retenues par le groupe avec le nombre de votes.

**Questions :**

A4a. Réécrivez vos 3 formulations HMW en précisant pour chacune : la frustration source (issue du Think-Aloud) et le niveau d'ambition (incrémental / ambitieux / rupture).

A4b. Quelle HMW a le plus influencé votre wireframe ? Montrez le lien direct entre la question HMW et un choix de design concret dans votre maquette.

---

### A5 — Design assisté par IA *(optionnel — bonus)*

> ⚠️ **Optionnel** : nécessite un accès à claude.ai ou ChatGPT.
> Si vous n'avez pas pu faire l'atelier, répondez uniquement à A5c (réflexion).

**Livrable :** Capture d'écran de votre échange avec le LLM + la réponse obtenue.

**Questions :**

A5a. Quelle commande du méta-prompt avez-vous utilisée ? Collez le prompt exact que vous avez envoyé.

A5b. La réponse du LLM était-elle **pertinente et utilisable** ? Avez-vous appliqué une de ses suggestions dans votre prototype ? Laquelle ?

A5c. *(Pour tous, même sans avoir fait l'atelier)* Un LLM peut générer des specs de composants et auditer du code pour la conformité RGAA. Selon vous, quelles tâches UX **ne peut-il pas** remplacer ? Justifiez en une ou deux phrases.

---

## Partie 1 — Analyse de l'application de référence

> Objectif : développer un regard critique d'UX designer sur une interface existante.

Explorez l'application de référence (`http://localhost:5173`) en vous mettant dans la peau de **Sophie**.

### 1.1 Première impression

**Questions :**

1. Sans lire aucune documentation, comprenez-vous immédiatement ce que fait cette application ? Décrivez ce que vous voyez en 2 phrases, comme si vous l'expliquiez à quelqu'un qui ne sait pas ce qu'est un code NAF ou ROME.

2. Combien de secondes vous faut-il pour effectuer votre première recherche ? Ce délai vous semble-t-il acceptable pour Sophie qui utilise l'outil plusieurs fois par jour ?

3. Listez **3 points forts** de l'interface actuelle (ce qui fonctionne bien pour Sophie).

4. Listez **3 points faibles** ou frustrations potentielles pour Sophie.

### 1.2 Psychologie cognitive

**Questions :**

5. **Loi de Miller** : combien de résultats s'affichent par défaut ? Est-ce conforme à la loi de Miller (7 ± 2 éléments) ? Vérifiez avec la valeur par défaut du sélecteur "lignes par page".

6. **Loi de Hick** : combien de filtres/options différents l'utilisateur voit-il sur la page principale ? Estimez le temps de décision que cela implique selon la loi de Hick. Y a-t-il trop de choix ?

7. **Loi de Fitts** : identifiez l'élément interactif le plus difficile à cliquer (petit, éloigné). Proposez une amélioration concrète.

8. **Gestalt — Proximité** : le code NAF et le libellé associé sont-ils visuellement groupés ? La disposition du tableau respecte-t-elle ce principe ?

9. **Gestalt — Similarité** : les badges NAF (bleu), ROME (violet) et Matching (vert) permettent-ils de distinguer les types immédiatement ? Ce choix de couleur vous semble-t-il intuitif pour Sophie ?

### 1.3 Scénario utilisateur

Réalisez ce scénario en tant que Sophie :

> *Sophie accompagne un candidat développeur. L'entreprise qui recrute a le code NAF `62.01Z`. Sophie veut trouver les métiers ROME compatibles pour orienter le candidat.*

**Questions :**

10. Décrivez **étape par étape** les actions que vous effectuez pour réaliser ce scénario (minimum 5 étapes).

11. À quelle étape avez-vous eu un doute ou une hésitation ? Pourquoi ?

12. L'application affiche-t-elle un **score de pertinence** pour les correspondances ? Pourquoi ce score est-il important pour Sophie qui doit justifier ses recommandations ?

---

## Partie 2 — Personas & User Stories

> Objectif : formaliser les besoins utilisateurs de manière structurée.

### 2.1 Fiche persona Sophie

Complétez cette fiche persona pour Sophie en vous basant sur le contexte du projet :

```
Nom : Sophie
Âge : 42 ans
Poste : Conseillère France Travail
Photo : [insérez une photo Unsplash libre de droits]

Objectifs :
- ...
- ...
- ...

Frustrations :
- ...
- ...
- ...

Contexte d'usage :
- Outil utilisé : ...
- Fréquence : ...
- Environnement : ...

Citation représentative :
"..."

Niveau technique : ⭐⭐☆☆☆
Niveau urgence : ⭐⭐⭐⭐☆
```

**Questions :**

13. Quelle est la différence entre un **persona** et un **utilisateur réel** ? Pourquoi crée-t-on des personas fictifs plutôt que de simplement interroger des utilisateurs ?

14. Sophie est décrite comme "peu habituée aux applications web avancées". Listez **3 implications concrètes** de ce trait sur les choix de design de l'interface (taille des boutons, vocabulaire, messages d'erreur…).

### 2.2 Fiche persona Karim

Créez la fiche complète de Karim en suivant le même format que Sophie.

**Questions :**

15. En quoi les besoins de Karim sont-ils **fondamentalement différents** de ceux de Sophie ? (type d'input, type d'output, contexte d'usage)

16. Karim n'a pas de compétences en API. Pourtant il a besoin du Service 2 (`POST /classify`). Qu'est-ce que cela implique pour l'interface ? L'API doit-elle être visible pour Karim ?

### 2.3 User Stories

Rédigez **8 user stories** au format `En tant que [persona], je veux [action] afin de [bénéfice]` :
- 3 pour Sophie (Service 1)
- 3 pour Karim (Service 2)
- 2 de votre choix (peuvent couvrir le mode vocal ou des besoins transverses)

**Questions :**

17. Parmi vos 8 user stories, laquelle vous semble la plus **critique** (à implémenter en priorité) ? Justifiez avec la méthode MoSCoW (Must / Should / Could / Won't).

18. Quelle user story vous semble la plus **difficile techniquement** à implémenter ? (Vous n'avez pas besoin de savoir comment — juste d'identifier la complexité.)

---

## Partie 3 — Design de l'interface Service 2 (Karim)

> Objectif : concevoir from scratch l'interface qui n'existe pas encore.

L'application de référence couvre uniquement le Service 1 (Sophie). Vous devez concevoir l'interface du Service 2 pour Karim.

### 3.1 Analyse du besoin

**Questions :**

19. Le Service 2 reçoit un texte libre (offre d'emploi, description d'entreprise) et retourne des codes NAF/ROME avec un score de confiance. Voici un exemple de réponse JSON attendue :
    ```json
    {
      "results": [
        {"code": "M1805", "type": "rome", "label": "Études et développement informatique", "score": 0.90},
        {"code": "62.01Z", "type": "naf", "label": "Programmation informatique", "score": 0.85}
      ],
      "justification": "Le texte mentionne 'développeur Python' et 'startup IA', fortement associés au domaine informatique."
    }
    ```
    Comment afficheriez-vous ce score de 90% à Sophie vs à Karim ? Sont-ce les mêmes besoins de lisibilité ?

20. Karim colle des textes souvent longs (plusieurs paragraphes). Quel composant UI choisiriez-vous pour la zone de saisie ? Justifiez (hauteur, redimensionnable, placeholder explicite…).

21. Comment indiquer visuellement à Karim que l'analyse IA est **en cours** (latence 1-3 secondes) ? Proposez 2 patterns UX différents et indiquez lequel vous choisissez et pourquoi.

### 3.2 Wireframe Service 2

Créez en **Excalidraw** le wireframe de l'interface Karim avec :
- La zone de saisie texte libre (grande, visible)
- Le bouton d'analyse
- L'indicateur de chargement
- Les résultats avec scores (ex : barre de progression ou pourcentage)
- La justification en langage naturel
- Un bouton "Nouvelle analyse" pour recommencer

**Questions :**

22. Dans votre wireframe, où placez-vous les résultats par rapport à la zone de saisie ? (en dessous, à droite, dans une modale…). Justifiez ce choix avec un principe cognitif.

23. Faut-il afficher le **JSON brut** de l'API à Karim ? Pourquoi ou pourquoi pas ?

24. Karim obtient un résultat avec score 45%. C'est incertain. Comment l'interface doit-elle communiquer cette **incertitude** sans alarmer l'utilisateur ?

---

## Partie 4 — Prototype haute fidélité

> Objectif : produire un prototype navigable et accessible dans Penpot ou Figma.

### 4.1 Design system minimal

Avant de prototyper, définissez votre design system en complétant ce tableau :

| Élément | Valeur choisie | Justification |
|---|---|---|
| Couleur primaire | | |
| Couleur secondaire | | |
| Couleur fond | | |
| Couleur texte principal | | |
| Contraste texte/fond | | ≥ 4.5:1 ? |
| Police titres | | |
| Police corps | | |
| Taille corps minimum | | ≥ 16px ? |
| Espacement de base | | Multiple de 8px ? |

**Questions :**

25. Vous choisissez une couleur de fond gris clair (`#F1F5F9`). Vérifiez sur [webaim.org/resources/contrastchecker](https://webaim.org/resources/contrastchecker) si le texte noir (`#1E293B`) donne un ratio de contraste conforme WCAG AA. Quel est le ratio obtenu ?

26. Quelle est la différence entre une **typographie à empattements** (serif) et **sans empattements** (sans-serif) ? Laquelle recommandez-vous pour une interface de travail utilisée plusieurs heures par jour ? Pourquoi ?

### 4.2 Composants

Dans votre prototype, créez et documentez ces composants :

**Questions :**

27. Le badge NAF est bleu, le badge ROME est violet, le badge Matching est vert. Un utilisateur daltonien rouge-vert peut-il encore distinguer les types ? Quelle modification apporteriez-vous ?

28. Concevez un composant "carte résultat" pour Karim qui affiche : le code, le libellé, le type (NAF/ROME), le score en %. Faites un croquis ou décrivez précisément sa structure.

29. Le prototype doit être navigable. Listez les **3 transitions** minimum que vous avez implémentées dans Penpot/Figma (ex : clic sur "Analyser" → affichage des résultats).

### 4.3 Mode vocal (bonus)

Si votre prototype intègre le mode vocal Whisper :

30. Comment l'utilisateur sait-il que l'application **écoute** ? Décrivez le feedback visuel (icône, animation, couleur).

31. Que se passe-t-il si la reconnaissance vocale échoue ou est imprécise ? Proposez un scénario d'erreur et son traitement UX.

---

## Partie 5 — RGAA dès le prototypage

> Objectif : intégrer l'accessibilité dans la conception, pas en post-correction.

### 5.1 Principes fondamentaux

**Questions :**

32. Expliquez en une phrase chacun des 4 principes WCAG **POUR** (Perceptible, Opérable, Compréhensible, Robuste) avec un exemple concret dans notre application.

33. Quelle est la différence entre **WCAG 2.1** et **RGAA 4.1** ? Le RGAA est-il obligatoire pour cette application ? (Indice : à qui s'applique l'obligation légale ?)

34. Un étudiant propose de signaler les erreurs de formulaire uniquement avec une bordure rouge. Citez **deux problèmes d'accessibilité** que cela pose et proposez une solution conforme.

### 5.2 Audit de votre prototype

Appliquez cette checklist à votre prototype Penpot/Figma :

| Critère RGAA | Conforme dans votre prototype ? | Observation |
|---|---|---|
| Contraste texte ≥ 4.5:1 | ✅ / ❌ | |
| Labels sur tous les champs | ✅ / ❌ | |
| Pas d'information par couleur seule | ✅ / ❌ | |
| Zones cliquables ≥ 44×44px | ✅ / ❌ | |
| Hiérarchie de titres logique | ✅ / ❌ | |
| Indicateur de focus prévu | ✅ / ❌ | |
| Messages d'erreur textuels | ✅ / ❌ | |
| Alternative texte aux icônes | ✅ / ❌ | |

**Questions :**

35. Pour le champ de saisie texte de Karim, quel attribut HTML garantit qu'un lecteur d'écran annonce son rôle ? (`placeholder` suffit-il ? Pourquoi ?)

36. Dans votre prototype, le bouton "Analyser" n'a qu'une icône loupe sans texte. Qu'est-ce que cela pose comme problème d'accessibilité ? Comment le corriger dans la maquette (sans toucher au code) ?

37. L'indicateur de chargement (spinner) que vous avez prévu est-il accessible ? Quel attribut `aria-*` doit accompagner un état de chargement dynamique ?

---

## Rendu attendu

Votre document de rendu doit contenir :

- [ ] **Photo** de la feuille Crazy 8s (8 esquisses papier)
- [ ] **Notes** du Think-Aloud (3 blocages documentés)
- [ ] **Tableau Nielsen** complété (10 heuristiques)
- [ ] **3 formulations HMW** + les 2 retenues par le groupe
- [ ] *(Optionnel)* Capture de l'échange LLM avec le méta-prompt
- [ ] Les réponses aux **questions A1 à A5** (ateliers) + aux **37 questions** numérotées
- [ ] La **fiche persona Sophie** complétée (avec photo)
- [ ] La **fiche persona Karim** créée (avec photo)
- [ ] Les **8 user stories**
- [ ] Le **wireframe Excalidraw** du Service 2 (Karim) exporté en PNG
- [ ] Le **prototype Penpot ou Figma** exporté (PDF ou lien de partage)
- [ ] La **checklist RGAA** complétée pour votre prototype
- [ ] Au minimum **5 captures d'écran annotées** (analyse de 03frontend + extraits de votre prototype)
- [ ] Une **conclusion** (10-15 lignes) : qu'avez-vous appris sur la conception UX ? Qu'est-ce qui vous a surpris ? Comment voyez-vous la relation entre UX et développement IA ?

---

## Ressources

| Ressource | URL |
|---|---|
| Application de référence | `03frontend/` → `./run.sh` → localhost:5173 |
| Méta-prompt Design IA *(optionnel)* | `METAPROMPT_design_naf_rome.md` |
| Excalidraw (wireframe) | https://excalidraw.com |
| Penpot (prototype) | https://penpot.app |
| WebAIM Contrast Checker | https://webaim.org/resources/contrastchecker/ |
| RGAA 4.1 officiel | https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/ |
| Loi de Miller | https://fr.wikipedia.org/wiki/Nombre_magique_(psychologie) |
| Loi de Hick | https://fr.wikipedia.org/wiki/Loi_de_Hick |
| Loi de Fitts | https://fr.wikipedia.org/wiki/Loi_de_Fitts |
| Gestalt principles | https://www.interaction-design.org/literature/topics/gestalt-principles |
| Unsplash (photos libres) | https://unsplash.com |
| DSFR Design Système État | https://www.systeme-de-design.gouv.fr/ |

---

*Évaluation conçue dans le cadre du Master IA · CreativeTech — TP 1.0 UX/UI NAF-ROME*
