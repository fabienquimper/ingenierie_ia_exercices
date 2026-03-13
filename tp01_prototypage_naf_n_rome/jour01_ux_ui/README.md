# TP 1.0 — UX/UI : Concevoir l'interface de l'application NAF-ROME

## Description

Avant de coder, on conçoit ! Ce TP vous apprend à penser l'expérience utilisateur
avant l'implémentation technique, en utilisant des outils de prototypage UI.

**Durée estimée :** 1 journée (7h)

---

## Wireframe de référence (Excalidraw)

Un wireframe complet de l'interface est fourni :  `wireframe_naf_rome.excalidraw`

Il représente les deux vues (Desktop 1400px + Mobile 390px) avec toutes les
fonctionnalités : recherche, filtres, tableau, export CSV, pagination.

### Ouvrir le wireframe

**Option A — En ligne (aucune installation)**
1. Allez sur **https://excalidraw.com**
2. `File → Open` → sélectionnez `wireframe_naf_rome.excalidraw`

**Option B — VS Code**
Installez l'extension [Excalidraw](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor)
puis ouvrez directement le fichier `.excalidraw`.

### Régénérer ou modifier le wireframe

Le fichier est généré par un script Python — vous pouvez le modifier librement :

```bash
# Régénérer après modification du script
python3 generate_wireframe.py
# → recrée wireframe_naf_rome.excalidraw
```

Le script `generate_wireframe.py` contient des fonctions simples (`rect`, `txt`, `arrow`)
que les étudiants peuvent modifier pour itérer sur le design.

### Interface prototype (Vue.js)

Le prototype fonctionnel (HTML/CSS/JS) est dans `frontend/` :

```bash
cd frontend && ./run.sh
# → http://localhost:5173
```

---

## Contexte

Vous devez concevoir l'interface d'une application web permettant aux conseillers
Pôle Emploi et aux RH d'entreprises de :

1. **Rechercher** des correspondances entre codes NAF et ROME
2. **Explorer** les métiers associés à une activité d'entreprise
3. **Valider** ou rejeter des correspondances suggérées par l'IA

---

## Outils de prototypage

### Option A : Penpot (Open Source, recommandé)
- **URL :** https://penpot.app
- **Avantage :** Gratuit, open source, collaborative
- **Tutoriel :** https://help.penpot.app/user-guide/, docker-compose: https://help.penpot.app/technical-guide/getting-started/docker/ (docker compose -p penpot -f docker-compose.yaml up -d, http://localhost:9001, docker compose -p penpot -f docker-compose.yaml down)
- **Démarrer :** Créez un compte, puis "New project"

### Option B : Figma (Freemium)
- **URL :** https://www.figma.com
- **Avantage :** Leader du marché, nombreuses ressources communautaires
- **Plan gratuit :** 3 fichiers, collaborateurs illimités en lecture
- **Tutoriel débutant :** https://help.figma.com/hc/en-us/articles/360038511533

### Option C : Excalidraw (fourni — recommandé pour démarrer)
- **URL :** https://excalidraw.com (style main levée, aucun compte requis)
- **Fichier fourni :** `wireframe_naf_rome.excalidraw` — wireframe de référence Desktop + Mobile
- **Ouvrir :** `File → Open` sur excalidraw.com, ou extension VS Code
- **Modifier :** relancez `python3 generate_wireframe.py` après édition du script
- **Draw.io :** https://draw.io (alternative offline possible)

---

## Livrables attendus

### 1. Personas (30 min)
Créez 2 personas représentant vos utilisateurs cibles :

**Persona 1 : Conseiller Pôle Emploi**
- Nom, âge, poste
- Objectifs : aider les demandeurs d'emploi à trouver des pistes de reconversion
- Frustrations : perte de temps à chercher dans des référentiels complexes
- Niveau technique : intermédiaire

**Persona 2 : Chargé de recrutement RH**
- Nom, âge, entreprise type
- Objectifs : trouver les bons profils ROME pour un poste NAF donné
- Frustrations : manque de connaissance des codes ROME
- Niveau technique : débutant à intermédiaire

### 2. User Stories (30 min)
Rédigez au minimum 5 user stories au format :
> En tant que **[persona]**, je veux **[action]** afin de **[bénéfice]**.

Exemples :
- En tant que **conseiller**, je veux **saisir un code NAF** afin de **voir les métiers ROME associés**.
- En tant que **RH**, je veux **rechercher par mot-clé** afin de **trouver le bon code NAF pour mon entreprise**.

### 3. Wireframes (2h)
Créez les maquettes basse fidélité des écrans suivants :

**Écran 1 : Page d'accueil / Recherche**
- Barre de recherche principale
- Filtres (par type : NAF ou ROME)
- Accès rapide aux codes populaires

**Écran 2 : Résultats de recherche**
- Liste des résultats avec score de pertinence
- Preview du code et de la description
- Possibilité de filtrer/trier

**Écran 3 : Détail d'une correspondance**
- Code NAF avec description complète
- Codes ROME associés (liste)
- Score de similarité visualisé

**Écran 4 : Vue mobile** (bonus)
- Version responsive de l'écran de recherche

### 4. Prototype interactif (2h)
Dans Figma ou Penpot, rendez votre prototype navigable :
- Cliquez sur la barre de recherche -> va vers les résultats
- Cliquez sur un résultat -> va vers le détail
- Bouton retour fonctionnel

---

## Critères d'évaluation UX

### Utilisabilité
- [ ] La recherche est visible et accessible immédiatement (principe de visibilité)
- [ ] Les codes NAF et ROME sont expliqués pour les non-experts
- [ ] Les erreurs sont présentées de façon compréhensible
- [ ] La pagination est intuitive

### Accessibilité (WCAG 2.1 niveau AA)
- [ ] Contraste suffisant (ratio 4.5:1 minimum pour le texte)
- [ ] Taille de police lisible (minimum 16px corps de texte)
- [ ] Navigation clavier possible
- [ ] Labels sur tous les champs de formulaire

### Cohérence visuelle
- [ ] Palette de couleurs définie et appliquée
- [ ] Typographie cohérente (2 polices max)
- [ ] Composants réutilisables (boutons, cartes, badges)
- [ ] Espacement régulier (grille de 8px)

---

## Ressources design

### Systèmes de design open source
- [Dsfr (Design Système de l'État)](https://www.systeme-de-design.gouv.fr/) - Recommandé pour une app gouvernementale
- [Material Design 3](https://m3.material.io/) - Google
- [Ant Design](https://ant.design/) - Enterprise

### Inspiration
- [Dribbble - UI Design](https://dribbble.com/tags/search-ui)
- [Mobbin - Patterns mobile/web](https://mobbin.com)
- [UI Patterns](https://ui-patterns.com)

### Couleurs accessibles
- [Coolors](https://coolors.co) - Générateur de palettes
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Paletton](https://paletton.com)

### Icônes
- [Heroicons](https://heroicons.com) (open source)
- [Lucide](https://lucide.dev) (open source)
- [Phosphor Icons](https://phosphoricons.com) (open source)

---

## Planning suggéré

| Heure | Activité |
|-------|----------|
| 09h00 - 09h30 | Introduction UX/UI — ouverture du wireframe de référence (`wireframe_naf_rome.excalidraw`) |
| 09h30 - 10h00 | Création des personas |
| 10h00 - 10h30 | Rédaction des user stories |
| 10h30 - 12h30 | Wireframes (4 écrans) — s'inspirer du wireframe fourni et itérer |
| 12h30 - 13h30 | Pause déjeuner |
| 13h30 - 15h30 | Prototype haute fidélité (couleurs, typo) |
| 15h30 - 16h30 | Liens interactifs dans le prototype |
| 16h30 - 17h00 | Présentation + feedback |

---

## Exercice bonus : Test utilisateur

Si le temps le permet, échangez votre prototype avec un autre groupe et effectuez
un test utilisateur rapide (5 minutes par personne) :

1. Donnez la tâche : "Trouvez les métiers ROME correspondant au code NAF 62.01Z"
2. Observez sans intervenir
3. Notez les blocages et incompréhensions
4. Utilisez le feedback pour itérer sur votre design

---

## Lien avec les TPs suivants

Le design que vous créez aujourd'hui servira de référence pour :
- **TP 1.1 (jour02)** : l'API que vous allez construire doit exposer les données
  nécessaires à votre interface — le prototype Vue.js est déjà disponible dans `frontend/`
- **Jour 5 (autonomie)** : vous pourrez implémenter et améliorer le prototype fonctionnel
