# Évaluation — Jour 2 : FastAPI NAF-ROME

**Niveau :** Master IA · CreativeTech  
**Durée estimée :** 3h30 à 4h  
**Rendu :** un document réponse (PDF ou Markdown) + captures d'écran annotées

---

## Progression depuis le Jour 1

Le Jour 2 fait évoluer l'application du Jour 1 en ajoutant une **API FastAPI** entre les données et le frontend.
L'interface Vue.js est visuellement identique — mais les données ne viennent plus de CSV chargés dans le navigateur,
elles transitent maintenant par un service Python.

| | Jour 1 | Jour 2 |
|---|---|---|
| Source des données | CSV → navigateur directement | CSV → Python → API → navigateur |
| Backend requis | Non | Oui (`localhost:8000`) |
| Fichier clé frontend | `csvService.ts` | `apiService.ts` |
| Indicateur connexion | Absent | Badge "API connectée / hors ligne" |

Observez dans `frontend/src/services/` les deux fichiers côte à côte :
- `csvService.ts` — l'approche Jour 1 (conservée pour comparaison)
- `apiService.ts` — l'approche Jour 2 (active)

---

## Avant de commencer

Assurez-vous que les deux services tournent :

```bash
# Terminal 1 — API backend
cd jour02_fast_api
./run.sh

# Terminal 2 — Frontend
cd jour02_fast_api/frontend
./run.sh
```

Vérifiez :
- API disponible sur [http://localhost:8000](http://localhost:8000)
- Frontend disponible sur [http://localhost:5174](http://localhost:5174)
- Documentation interactive sur [http://localhost:8000/docs](http://localhost:8000/docs)

**Question préliminaire :** Ouvrez les DevTools du navigateur (F12 → onglet **Network**). Rechargez la page.
Quel appel réseau part vers `localhost:8000` ? Comparez avec le Jour 1 où vous verriez des appels vers des fichiers `.csv` locaux. Quelle différence d'architecture cela illustre-t-il ?

---

## Partie 1 — Je joue avec l'API (Swagger / curl)

> Objectif : comprendre comment fonctionne une API REST en l'interrogeant directement, sans passer par l'interface graphique.

### 1.1 Découverte de la documentation automatique

Ouvrez [http://localhost:8000/docs](http://localhost:8000/docs).

**Questions :**

1. Combien d'endpoints (routes) l'API expose-t-elle ? Listez-les avec leur méthode HTTP (GET / POST).
2. Quelle est la différence entre un endpoint `GET` et un endpoint `POST` ? Donnez un exemple dans cette API.
3. Qu'est-ce que Swagger UI ? Quel standard il implémente (OpenAPI) et à quoi sert ce standard ?
4. Trouvez l'endpoint `/health`. À quoi sert un endpoint de ce type dans une vraie application en production ?

### 1.2 Tester les endpoints via Swagger

Pour chaque endpoint ci-dessous, cliquez sur "Try it out", renseignez les paramètres, exécutez et **notez la réponse JSON complète** :

| Endpoint | Paramètres à tester | Ce que vous observez |
|---|---|---|
| `GET /health` | aucun | |
| `GET /api/v1/naf` | `limit=5` | |
| `GET /api/v1/rome` | `limit=5, offset=10` | |
| `GET /api/v1/naf/{code_naf}` | `62.01Z` | |
| `GET /api/v1/rome/{code_rome}` | `M1805` | |
| `GET /api/v1/mapping/naf-to-rome/{code_naf}` | `62.01Z` | |
| `POST /api/v1/search` | `{"query": "informatique", "limit": 5}` | |

**Questions :**

5. Que contient le champ `total` dans la réponse de `GET /api/v1/naf` ? À quoi sert-il côté frontend ?
6. Testez `GET /api/v1/naf/{code_naf}` avec un code inexistant (ex: `99.99Z`). Quel code HTTP recevez-vous ? Que signifie ce code ?
7. Testez `POST /api/v1/search` avec une requête vide `{"query": "", "limit": 5}`. Que se passe-t-il ? Est-ce le comportement attendu selon vous ?
8. Quelle est la différence entre `GET /api/v1/rome/{code_rome}` (détail) et `GET /api/v1/mapping/rome-to-naf/{code_rome}` (correspondances) ?

### 1.3 Tester avec curl (terminal)

Reproduisez les mêmes appels depuis un terminal :

```bash
# Santé de l'API
curl http://localhost:8000/health

# Liste des codes NAF (5 premiers)
curl "http://localhost:8000/api/v1/naf?limit=5"

# Recherche par mot-clé
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "agriculture", "limit": 3}'
```

**Questions :**

9. Quelle est la différence pratique entre tester via Swagger et tester via curl ? Dans quel contexte utiliseriez-vous l'un ou l'autre ?
10. Ajoutez l'option `-v` à votre commande curl (`curl -v http://localhost:8000/health`). Identifiez dans la sortie : la méthode HTTP, le code de statut, le Content-Type de la réponse et au moins un header HTTP.

### 1.4 Comprendre les codes de statut HTTP

Complétez ce tableau à partir de vos tests :

| Code | Nom | Quand l'API le renvoie | Exemple observé |
|---|---|---|---|
| 200 | OK | | |
| 404 | Not Found | | |
| 422 | Unprocessable Entity | | |
| 500 | Internal Server Error | | |

**Question :**

11. Cherchez ce qu'est le code `422 Unprocessable Entity`. Testez-le en envoyant un body invalide à `POST /api/v1/search` (par exemple `{"query": 123}`). Décrivez la réponse d'erreur obtenue.

---

## Partie 2 — UX/UI de l'API (design d'interface pour développeurs)

> Une API est une interface — mais pour des développeurs. Elle a aussi une UX : la cohérence des routes, la lisibilité des réponses, la qualité de la documentation.

### 2.1 Cohérence et nommage des routes

Examinez la liste complète des endpoints de l'API.

**Questions :**

12. Les routes suivent-elles une convention cohérente ? Identifiez le préfixe commun et expliquez ce que signifie `/api/v1/`.
13. Pourquoi versionner une API (le `/v1`) ? Que se passerait-il si vous modifiez une réponse sans versioning alors que des applications tierces consomment votre API ?
14. Comparez ces deux URLs hypothétiques : `GET /api/v1/getNafByCode?code=62.01Z` vs `GET /api/v1/naf/62.01Z`. Laquelle respecte les conventions REST ? Pourquoi ?

### 2.2 Structure des réponses JSON

Observez les réponses de `GET /api/v1/naf?limit=5` et `GET /api/v1/naf/62.01Z`.

**Questions :**

15. La réponse de la liste inclut-elle des métadonnées de pagination (`total`, `limit`, `offset`) ? Pourquoi ces champs sont-ils importants pour un frontend ?
16. Les champs sont-ils cohérents d'un endpoint à l'autre ? Y a-t-il des différences dans les noms de champs entre la liste et le détail ?
17. L'API renvoie-t-elle des messages d'erreur lisibles par un humain ? Comparez un 404 et un 422 et évaluez leur clarté.

### 2.3 Documentation et expérience développeur (DX)

**Questions :**

18. Ouvrez `/docs` et `/redoc` (deux interfaces différentes pour la même spec OpenAPI). Laquelle préférez-vous pour découvrir une API ? Laquelle pour l'utiliser au quotidien ?
19. Les descriptions des endpoints dans Swagger sont-elles suffisamment explicites pour qu'un développeur externe comprenne comment utiliser l'API sans lire le code source ?
20. Proposez 2 améliorations concrètes que vous apporteriez au design de cette API (nouveaux endpoints, meilleure gestion des erreurs, champs supplémentaires, etc.).

---

## Partie 3 — UX/UI du Frontend

> Objectif : évaluer l'interface utilisateur de l'application Vue.js à travers des scénarios réels d'utilisation.

### 3.1 Scénarios d'usage

Ouvrez le frontend sur [http://localhost:5174](http://localhost:5174) et réalisez les scénarios suivants :

**Scénario A — Trouver les métiers liés à l'informatique**
1. Tapez "informatique" dans la barre de recherche
2. Filtrez sur "ROME" uniquement
3. Notez combien de résultats vous obtenez et évaluez leur pertinence

**Scénario B — Rechercher par code**
1. Saisissez le code `62.01Z` dans le champ code
2. Que se passe-t-il si vous tapez `6201Z` (sans le point) ? L'application gère-t-elle bien ce cas ?

**Scénario C — Explorer les correspondances**
1. Filtrez sur "Matching NAF↔ROME"
2. Exportez les résultats en CSV
3. Ouvrez le fichier exporté : les données sont-elles correctes ?

### 3.2 Questions d'évaluation UX

21. **Affordance** : sans lire de documentation, comprenez-vous immédiatement à quoi sert chaque élément de l'interface ? Identifiez 1 élément clair et 1 élément ambigu.
22. **Feedback** : l'application vous informe-t-elle de son état (chargement, erreur, aucun résultat) ? Décrivez les messages de feedback observés.
23. **Efficacité** : combien de clics/actions sont nécessaires pour trouver les métiers ROME correspondant au code NAF `62.01Z` ? Ce nombre vous semble-t-il optimal ?
24. **Cohérence visuelle** : les badges de couleur (bleu NAF, violet ROME, vert Matching) vous semblent-ils intuitifs ? Proposez une légende qui pourrait aider les nouveaux utilisateurs.
25. **Responsive** : réduisez la fenêtre du navigateur à 375px de large (mobile). L'interface reste-t-elle utilisable ? Notez les problèmes observés.
26. **Performance perçue** : au chargement initial, l'application affiche-t-elle un indicateur de progression ? L'attente vous semble-t-elle acceptable ?

### 3.3 Propositions d'amélioration

27. Listez **3 améliorations UX prioritaires** que vous implémenterez en vous basant sur vos observations. Pour chacune, précisez : le problème observé, la solution proposée, et l'impact attendu sur l'utilisateur.

---

## Partie 4 — Accessibilité RGAA & WCAG

> Le RGAA (Référentiel Général d'Amélioration de l'Accessibilité) est le standard français d'accessibilité web, obligatoire pour les services publics. Il est basé sur les WCAG 2.1 (Web Content Accessibility Guidelines) du W3C.

### 4.1 Contexte et enjeux

**Questions préliminaires :**

28. Qu'est-ce que l'accessibilité numérique ? Citez 4 types de handicaps différents que l'accessibilité web vise à compenser.
29. Quelle est la différence entre le RGAA (version 4.1) et les WCAG 2.1 ? Lequel est obligatoire en France et pour quels organismes ?
30. Les WCAG définissent 3 niveaux de conformité : A, AA, AAA. Que signifient-ils ? Quel niveau minimum est généralement requis ?

### 4.2 Installation de l'extension WAVE

WAVE (Web Accessibility Evaluation Tool) est un outil d'audit d'accessibilité développé par WebAIM.

**Étapes d'installation :**
1. Ouvrez Chrome et allez dans le Chrome Web Store
2. Recherchez **"WAVE Evaluation Tool"** (éditeur : WebAIM)
3. Cliquez sur "Ajouter à Chrome"
4. Une fois installée, l'icône WAVE apparaît dans votre barre d'extensions

**Prise en main :**
1. Naviguez vers [http://localhost:5174](http://localhost:5174)
2. Cliquez sur l'icône WAVE
3. Explorez les 5 onglets : **Summary**, **Details**, **Reference**, **Structure**, **Contrast**

**Questions :**

31. Combien d'erreurs (rouge), d'alertes (jaune) et d'éléments structurels WAVE détecte-t-il sur notre frontend ?
32. Cliquez sur une erreur dans l'onglet "Details". WAVE vous indique le critère WCAG violé : notez-le et expliquez ce que ce critère demande.
33. Ouvrez l'onglet "Contrast" : y a-t-il des problèmes de contraste détectés ? Quel est le ratio de contraste minimum requis par WCAG 2.1 AA pour du texte normal ?

### 4.3 Les 4 principes WCAG (POUR)

Les WCAG s'organisent autour de 4 principes : **P**erceptible, **O**pérable, **C**ompréhensible, **R**obuste.

#### Principe 1 — Perceptible

Toute l'information doit être présentable de façon à ce que les utilisateurs puissent la percevoir.

| Critère | Niveau | Description | Test sur notre app |
|---|---|---|---|
| **1.1.1** Contenu non textuel | A | Toute image doit avoir un attribut `alt` descriptif | |
| **1.3.1** Information et relations | A | La structure (titres, listes, tableaux) doit être sémantique | |
| **1.3.2** Ordre séquentiel | A | L'ordre de lecture dans le code doit correspondre à l'ordre visuel | |
| **1.3.3** Caractéristiques sensorielles | A | Ne pas dépendre uniquement de la couleur, forme ou position | |
| **1.3.4** Orientation | AA | Ne pas bloquer l'affichage en mode portrait ou paysage | |
| **1.4.1** Utilisation de la couleur | A | La couleur ne doit pas être le seul moyen de transmettre une info | |
| **1.4.3** Contraste (minimum) | AA | Texte normal ≥ 4.5:1 / Grand texte ≥ 3:1 | |
| **1.4.4** Redimensionnement | AA | Le texte doit rester lisible jusqu'à 200% de zoom | |
| **1.4.10** Redistribution | AA | Pas de défilement horizontal à 320px de large | |
| **1.4.11** Contraste des éléments non textuels | AA | Icônes, champs de formulaire ≥ 3:1 | |
| **1.4.12** Espacement du texte | AA | L'espacement des lignes/lettres doit pouvoir être modifié | |
| **1.4.13** Contenu au survol | AA | Info-bulles et menus doivent rester accessibles | |

**Questions :**

34. Inspectez le code HTML de notre frontend (F12 → Elements). Les images et icônes SVG ont-elles des attributs `alt` ou `aria-label` ?
35. Testez le critère 1.4.3 : utilisez l'outil "Contrast Checker" de WebAIM (en ligne) sur la couleur du texte gris clair des descriptions (`text-slate-500`). Le ratio est-il conforme ?
36. Testez le critère 1.4.10 : réduisez le zoom du navigateur à 320px de large (ou utilisez les DevTools en mode responsive). Y a-t-il un défilement horizontal ?
37. Testez le critère 1.4.4 : appuyez sur `Ctrl + +` jusqu'à 200% de zoom. Le tableau reste-t-il lisible ? Des éléments se chevauchent-ils ?

#### Principe 2 — Opérable

Les composants d'interface et la navigation doivent être utilisables.

| Critère | Niveau | Description | Test sur notre app |
|---|---|---|---|
| **2.1.1** Clavier | A | Toutes les fonctionnalités accessibles au clavier | |
| **2.1.2** Pas de piège clavier | A | Le focus ne doit jamais rester bloqué | |
| **2.4.1** Contournement de blocs | A | Un lien "Aller au contenu" doit permettre de sauter la navigation | |
| **2.4.2** Titre de page | A | La page doit avoir un `<title>` descriptif et unique | |
| **2.4.3** Parcours du focus | A | L'ordre du focus Tab doit être logique | |
| **2.4.4** Fonction du lien | A | Le texte du lien doit être compréhensible hors contexte | |
| **2.4.6** En-têtes et étiquettes | AA | Les titres et labels doivent être descriptifs | |
| **2.4.7** Focus visible | AA | L'indicateur de focus clavier doit être visible | |

**Questions :**

38. Naviguez sur notre frontend **uniquement au clavier** (Tab, Shift+Tab, Entrée, Espace). Pouvez-vous : rechercher un terme, filtrer par type, naviguer entre les pages ? Notez les blocages éventuels.
39. Appuyez sur Tab depuis le début de la page. L'ordre de navigation est-il logique ? L'indicateur de focus (outline) est-il toujours visible ?
40. Vérifiez dans le code source HTML que la page a un `<title>` défini. Est-il descriptif ?
41. Le critère 2.4.1 recommande un lien "Aller au contenu principal". Notre application en a-t-elle un ? Pourquoi est-ce important pour un utilisateur de lecteur d'écran ?

#### Principe 3 — Compréhensible

L'information et l'utilisation de l'interface doivent être compréhensibles.

| Critère | Niveau | Description | Test sur notre app |
|---|---|---|---|
| **3.1.1** Langue de la page | A | L'attribut `lang` sur `<html>` doit indiquer la langue | |
| **3.1.2** Langue des parties | AA | Les passages en langue étrangère doivent être balisés | |
| **3.2.1** Au focus | A | Le focus ne doit pas déclencher de changement de contexte | |
| **3.2.2** À la saisie | A | Saisir ne doit pas déclencher de changement inattendu | |
| **3.3.1** Identification des erreurs | A | Les erreurs doivent être identifiées et décrites textuellement | |
| **3.3.2** Étiquettes ou instructions | A | Les champs de formulaire doivent avoir des labels | |
| **3.3.3** Suggestion après une erreur | AA | Des suggestions doivent être proposées en cas d'erreur | |

**Questions :**

42. Inspectez le `<html>` de notre page. L'attribut `lang="fr"` est-il présent ?
43. Les champs de recherche ont-ils des `<label>` associés (via `for`/`id` ou `aria-label`) ? Testez en passant le focus sur le champ de recherche avec un lecteur d'écran ou en inspectant le DOM.
44. Tapez une valeur dans le champ de recherche. Un lecteur d'écran annonce-t-il le nombre de résultats mis à jour dynamiquement ? (indice : vérifiez si des attributs `aria-live` sont présents).

#### Principe 4 — Robuste

Le contenu doit être suffisamment robuste pour être interprété par les technologies d'assistance.

| Critère | Niveau | Description | Test sur notre app |
|---|---|---|---|
| **4.1.1** Analyse syntaxique | A | Le HTML doit être valide (balises correctement imbriquées) | |
| **4.1.2** Nom, rôle, valeur | A | Tous les composants UI doivent avoir un nom et un rôle accessibles | |
| **4.1.3** Messages d'état | AA | Les messages de statut doivent être lisibles sans prendre le focus | |

**Questions :**

45. Validez le HTML de notre page via le [validateur W3C](https://validator.w3.org/) (option "Validate by URI" avec une URL publique, ou "Validate by Direct Input" en copiant le source). Combien d'erreurs et d'avertissements obtenez-vous ?
46. Inspectez les boutons de filtre (NAF, ROME, Matching) : ont-ils des attributs `role`, `aria-pressed` ou `aria-selected` pour indiquer leur état aux technologies d'assistance ?
47. Lorsque les données se chargent, y a-t-il un message d'état (`aria-live="polite"`) qui annonce la fin du chargement aux utilisateurs de lecteurs d'écran ?

### 4.4 Les 13 thèmes RGAA 4.1

Le RGAA 4.1 organise ses 106 critères en 13 thèmes. Voici une grille d'auto-évaluation rapide pour notre application :

| # | Thème RGAA | Applicable ? | Conforme ? | Observations |
|---|---|---|---|---|
| 1 | Images | Oui/Non | ✅/❌/NA | |
| 2 | Cadres (iframes) | Oui/Non | ✅/❌/NA | |
| 3 | Couleurs | Oui | | |
| 4 | Multimédia | Oui/Non | ✅/❌/NA | |
| 5 | Tableaux | Oui | | |
| 6 | Liens | Oui | | |
| 7 | Scripts | Oui | | |
| 8 | Éléments obligatoires | Oui | | |
| 9 | Structuration de l'information | Oui | | |
| 10 | Présentation de l'information | Oui | | |
| 11 | Formulaires | Oui | | |
| 12 | Navigation | Oui | | |
| 13 | Consultation | Oui | | |

**Questions :**

48. Pour le thème **5 (Tableaux)** : notre tableau de résultats utilise-t-il les balises sémantiques correctes (`<th scope="col">`, `<caption>`) ? Inspectez le HTML.
49. Pour le thème **9 (Structuration)** : la page utilise-t-elle une hiérarchie de titres logique (`h1` → `h2` → `h3`) ? Utilisez WAVE onglet "Structure" pour visualiser.
50. Pour le thème **11 (Formulaires)** : les champs de saisie ont-ils des labels visibles ET des attributs `autocomplete` appropriés ?

---

## Partie 5 — Audit de 5 sites avec WAVE

> Objectif : comparer le niveau d'accessibilité de sites réels et comprendre que même les grandes organisations ont des progrès à faire.

### Méthodologie d'audit

Pour chaque site, auditez **5 pages différentes** (page d'accueil + 4 autres pages représentatives).  
Pour chaque page, notez avec WAVE :
- Nombre d'**erreurs** (rouge)
- Nombre d'**alertes** (jaune)  
- Nombre d'éléments de **structure** détectés
- Présence d'un **lien d'évitement** (skip link)
- Conformité de la **langue** (`lang` attribute)
- Présence de **titres alternatifs** sur les images principales

Utilisez cette grille pour chaque site :

```
Site : _______________
URL : _______________

| Page | URL | Erreurs | Alertes | Structure | Skip link | Lang |
|------|-----|---------|---------|-----------|-----------|------|
| Accueil | | | | | | |
| Page 2 | | | | | | |
| Page 3 | | | | | | |
| Page 4 | | | | | | |
| Page 5 | | | | | | |

Points forts observés :
Points faibles observés :
Note globale /10 :
```

### Sites à auditer

#### Site 1 — Wikipédia France
**URL de départ :** https://fr.wikipedia.org  
**Pages suggérées :** Accueil, un article court, un article avec tableau, la page de recherche, une page de catégorie  
**Point d'attention particulier :** Wikipédia a une politique d'accessibilité active. Comparez les images avec et sans légende.

#### Site 2 — Le Monde
**URL de départ :** https://www.lemonde.fr  
**Pages suggérées :** Accueil, un article, la page Politique, la page Économie, la page de recherche  
**Point d'attention particulier :** Observez comment les publicités affectent les scores d'accessibilité. Le contenu payant est-il accessible ?

#### Site 3 — Le Bon Coin
**URL de départ :** https://www.leboncoin.fr  
**Pages suggérées :** Accueil, une page de catégorie, une annonce, la page de dépôt d'annonce, la page de connexion  
**Point d'attention particulier :** Observez l'accessibilité des formulaires et des images d'annonces.

#### Site 4 — Info.gouv.fr
**URL de départ :** https://www.info.gouv.fr  
**Pages suggérées :** Accueil, une actualité, la page "Le Gouvernement", une page de service public, la page Contact  
**Point d'attention particulier :** Ce site est soumis au RGAA obligatoire. Cherchez leur déclaration d'accessibilité (souvent en bas de page).

#### Site 5 — WAVE WebAIM
**URL de départ :** https://wave.webaim.org  
**Pages suggérées :** Accueil, la page Documentation, la page des extensions, les résultats d'un audit (lancez une analyse), la page À propos  
**Point d'attention particulier :** Un outil d'accessibilité est-il lui-même accessible ? Comparez son score avec les autres.

### Questions de synthèse sur l'audit

51. Quel site obtient le meilleur score global d'accessibilité selon vous ? Était-ce celui que vous attendiez ? Pourquoi ?
52. Info.gouv.fr est soumis au RGAA obligatoirement. Trouvez sa déclaration d'accessibilité (lien en bas de page). Quel niveau de conformité est revendiqué ? Les erreurs WAVE contredisent-elles cette déclaration ?
53. Le Bon Coin est un site commercial. Les erreurs d'accessibilité identifiées impactent-elles des fonctionnalités critiques (ex: déposer une annonce, contacter un vendeur) ?
54. Sur Wikipédia, toutes les images ont-elles un attribut `alt` ? Qu'en est-il des formules mathématiques ou des graphiques SVG ?
55. Comparez le score de WAVE WebAIM avec celui des autres sites. Quelle conclusion tirez-vous sur la relation entre "outil d'accessibilité" et "site accessible" ?

### Tableau de synthèse comparative

Remplissez ce tableau final :

| Site | Moy. erreurs/page | Moy. alertes/page | Skip link | Déclaration RGAA | Note /10 |
|---|---|---|---|---|---|
| Wikipédia FR | | | | | |
| Le Monde | | | | | |
| Le Bon Coin | | | | | |
| Info.gouv.fr | | | Oui/Non | | |
| WAVE WebAIM | | | | | |
| **Notre app** | | | | NA | |

56. Notre application figure dans ce tableau. Comment se situe-t-elle par rapport aux sites professionnels audités ? Quelles sont les 3 améliorations d'accessibilité les plus urgentes à apporter à notre frontend ?

---

## Rendu attendu

Votre document de rendu doit contenir :

- [ ] Les réponses aux **56 questions** numérotées
- [ ] Le tableau complété de l'**audit WAVE** pour les 5 sites × 5 pages
- [ ] Le **tableau de synthèse** comparative
- [ ] La **grille RGAA** complétée pour notre application
- [ ] Au minimum **10 captures d'écran** annotées (erreurs WAVE, tests clavier, comparaisons de contraste, etc.)
- [ ] Une **conclusion personnelle** (15-20 lignes) : qu'avez-vous appris sur l'accessibilité ? Qu'est-ce qui vous a surpris ? Comment intégrerez-vous ces pratiques dans vos futurs projets ?

---

## Ressources

| Ressource | URL |
|---|---|
| RGAA 4.1 (officiel) | https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/ |
| WCAG 2.1 (W3C) | https://www.w3.org/TR/WCAG21/ |
| WCAG Quick Reference | https://www.w3.org/WAI/WCAG21/quickref/ |
| Extension WAVE Chrome | https://wave.webaim.org/extension/ |
| Contrast Checker WebAIM | https://webaim.org/resources/contrastchecker/ |
| Validateur HTML W3C | https://validator.w3.org/ |
| Simulateur de handicap (NoCoffee) | https://chrome.google.com/webstore/detail/nocoffee |
| Déclaration RGAA info.gouv.fr | https://www.info.gouv.fr/accessibilite |

---

*Évaluation conçue dans le cadre du Master IA · CreativeTech — TP 1.1 FastAPI NAF-ROME*
