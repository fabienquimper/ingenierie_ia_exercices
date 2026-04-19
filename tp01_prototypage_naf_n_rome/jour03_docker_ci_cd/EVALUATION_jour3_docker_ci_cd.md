# Évaluation — Jour 3 : Docker & CI/CD

**Niveau :** Master IA · CreativeTech  
**Durée estimée :** 3h30 à 4h  
**Rendu :** un document réponse (PDF ou Markdown) + captures d'écran annotées

---

## Progression depuis les Jours 1 et 2

Le Jour 3 containerise l'application construite aux jours précédents. Rien ne change fonctionnellement — mais le **mode de livraison** change radicalement.

| | Jour 1 | Jour 2 | Jour 3 |
|---|---|---|---|
| Source données | CSV → navigateur | CSV → API → navigateur | Idem, dans Docker |
| Lancement | `npm run dev` | `uvicorn` + `npm run dev` | `docker compose up` |
| Tests | Manuels | `pytest` local | `pytest` dans stage Docker |
| Déployable sur un serveur ? | Non | Partiellement | Oui, n'importe où |

---

## Avant de commencer

Assurez-vous que Docker est installé et fonctionnel :

```bash
docker --version
docker compose version
```

Construisez et démarrez l'application :

```bash
cd jour03_docker_ci_cd
docker compose up --build -d
```

Vérifiez avec ces commandes :

```bash
# 1. Les conteneurs sont bien actifs
docker ps

# Résultat attendu : 2 conteneurs "Up ... (healthy)"
# NAMES            IMAGE                PORTS                    STATUS
# naf_rome_api     naf-rome-api:latest  0.0.0.0:8000->8000/tcp   Up X minutes (healthy)
# naf_rome_redis   redis:7-alpine       0.0.0.0:6379->6379/tcp   Up X minutes (healthy)

# 2. L'API répond et a bien chargé les 3 fichiers de données
curl http://localhost:8000/health

# Résultat attendu :
# {"status": "ok", "version": "1.0.0", "records_loaded": 23195}
```

Points à vérifier :
- Statut `(healthy)` sur les deux conteneurs — pas `starting` ni `unhealthy`
- `records_loaded: 23195` — si 0, les CSV n'ont pas été trouvés
- Documentation interactive : http://localhost:8000/docs
- Frontend Jour 2 accessible : http://localhost:5174 (si lancé séparément)

**Question préliminaire A :** Comparez la commande de démarrage du Jour 2 (`uvicorn app.main:app --reload`) et celle du Jour 3 (`docker compose up --build`). Quelle information supplémentaire Docker Compose prend-il en charge que vous deviez gérer manuellement au Jour 2 ?

**Question préliminaire B :** Lancez l'API avec `docker compose up -d`, puis lancez le frontend du Jour 2 (`cd ../jour02_fast_api/frontend && ./run.sh`). Le frontend se connecte-t-il à l'API ? Ouvrez les DevTools (F12 → Network) et confirmez que les appels vont bien vers `localhost:8000`. Que démontre ce test sur la notion d'**isolation** qu'apporte Docker ?

---

## Partie 1 — Comprendre Docker

> Objectif : maîtriser les concepts fondamentaux de Docker à travers l'analyse du Dockerfile de ce projet.

### 1.1 Images et conteneurs

**Questions :**

1. Quelle est la différence entre une **image Docker** et un **conteneur Docker** ? Utilisez une analogie (ex : classe/instance, recette/plat cuisiné).
2. Lancez `docker images` après le build. Quelle est la taille de l'image `naf-rome-api` ? Pourquoi est-il important de minimiser la taille d'une image ?
3. Lancez `docker ps`. Quels conteneurs sont actifs ? Identifiez leur nom, image, ports exposés et statut.
4. Quelle est la différence entre `docker run` et `docker compose up` ? Dans quel cas utiliseriez-vous l'un ou l'autre ?

### 1.2 Le Dockerfile multi-stage

Ouvrez le fichier `Dockerfile` et analysez ses 3 stages : `builder`, `test`, `runtime`.

**Questions :**

5. Pourquoi utilise-t-on un build multi-stage ? Quel problème cela résout-il par rapport à un Dockerfile à stage unique ?
6. Que fait l'instruction `COPY --from=builder` dans le stage `runtime` ? Pourquoi ne pas simplement utiliser `FROM builder AS runtime` ?
7. Pourquoi le stage `runtime` n'installe-t-il pas les dépendances de dev (pytest, ruff, etc.) ? Quel impact cela a-t-il sur l'image finale ?
8. L'instruction `USER appuser` apparaît dans le stage `runtime`. Pourquoi est-ce une bonne pratique de sécurité de ne pas faire tourner l'application en tant que `root` ?
9. Que fait l'instruction `HEALTHCHECK` ? Comment Docker l'utilise-t-il ? Vérifiez l'état du healthcheck avec `docker inspect naf_rome_api | grep -A 10 Health`.

### 1.3 Layers et cache Docker

**Questions :**

10. Lancez `docker build -t naf-rome-api:local .` deux fois de suite. Observez la sortie la deuxième fois : quelles lignes affichent `CACHED` ? Expliquez pourquoi le cache Docker fonctionne ainsi.
11. Pourquoi copie-t-on `pyproject.toml` **avant** `COPY app/ ./app/` dans le builder ? Que se passerait-il si on inversait l'ordre ?
12. Qu'est-ce que le fichier `.dockerignore` ? Listez 3 types de fichiers/dossiers qu'on devrait exclure et expliquez pourquoi.

### 1.4 Le stage test comme gardien qualité

**Questions :**

13. Lancez `docker build --target test -t naf-rome-test .`. Que se passe-t-il si un test échoue ? Le build continue-t-il ? Pourquoi est-ce important en CI/CD ?
14. Combien de tests passent ? Quel est le code de sortie (`echo $?`) quand tous les tests passent ? Et quand l'un échoue ?
15. Comparez cette approche (tests dans Docker) avec `pytest tests/ -v` en local. Quels avantages offre l'approche Docker pour une équipe distribuée ?

---

## Partie 2 — Docker Compose

> Objectif : comprendre l'orchestration multi-conteneurs et la configuration déclarative.

### 2.1 Anatomie du docker-compose.yml

Ouvrez `docker-compose.yml`.

**Questions :**

16. Combien de services sont définis ? Listez-les avec leur image et leur port.
17. Qu'est-ce que `depends_on` avec `condition: service_healthy` ? Pourquoi est-ce mieux que `depends_on` seul (sans condition) ?
18. Le service `api` monte un volume `./data:/app/data:ro`. Expliquez chaque partie de cette syntaxe. Que signifie `:ro` et pourquoi l'utilise-t-on ici ?
19. Qu'est-ce qu'un réseau Docker (`naf_rome_net`) ? Pourquoi les services dans le même réseau peuvent-ils se parler par leur nom de service (ex: `redis://redis:6379`) sans connaître leur IP ?

### 2.2 Variables d'environnement

**Questions :**

20. Les 3 variables `APP_DATA_NAF_PATH`, `APP_DATA_ROME_PATH`, `APP_DATA_MATCHING_PATH` dans le docker-compose correspondent à quoi dans le code Python ? (indice : ouvrez `app/config.py`)
21. Modifiez temporairement `APP_DATA_NAF_PATH` avec une valeur invalide dans docker-compose.yml, relancez et observez l'erreur. Remettez la valeur correcte ensuite. Quel est l'intérêt de configurer via des variables d'environnement plutôt qu'en dur dans le code ?
22. Quelle est la différence entre passer des variables d'environnement dans docker-compose.yml et les stocker dans un fichier `.env` ? Dans quel cas utiliseriez-vous chaque approche ?

### 2.3 Commandes Docker Compose essentielles

Exécutez et observez les commandes suivantes. Pour chacune, notez ce qu'elle fait et dans quel contexte l'utiliser :

| Commande | Ce qu'elle fait | Quand l'utiliser |
|---|---|---|
| `docker compose up --build -d` | | |
| `docker compose logs -f api` | | |
| `docker compose exec api bash` | | |
| `docker compose ps` | | |
| `docker compose down` | | |
| `docker compose down -v` | | |

**Questions :**

23. Quelle est la différence entre `docker compose down` et `docker compose down -v` ? Dans quel cas la différence est-elle importante ?
24. Lancez `docker compose exec api python -c "from app.services.matcher import get_matcher; m = get_matcher(); print(m.record_count)"`. Que retourne cette commande ? À quoi sert `docker compose exec` ?

---

## Partie 3 — Tests et qualité du code

> Objectif : comprendre comment les tests garantissent la fiabilité d'une API en production.

### 3.1 Architecture des tests

Ouvrez `tests/conftest.py` et `tests/test_mapping.py`.

**Questions :**

25. Qu'est-ce qu'un fichier `conftest.py` dans pytest ? Quel rôle joue-t-il par rapport aux fichiers `test_*.py` ?
26. La fixture `load_test_data` utilise `tmp_path`. Qu'est-ce que `tmp_path` ? Pourquoi crée-t-on des CSV temporaires plutôt que d'utiliser les vrais fichiers de données ?
27. La fixture est décorée `@pytest.fixture(autouse=True)`. Que signifie `autouse=True` ? Comparez avec une fixture non-autouse.
28. Pourquoi les tests créent-ils 3 CSV séparés (naf, rome, matching) plutôt qu'un seul CSV avec une colonne `type` ?

### 3.2 Analyse des tests existants

**Questions :**

29. Lancez les tests avec couverture :
    ```bash
    source ../jour02_fast_api/.venv/bin/activate
    pytest tests/ -v --cov=app --cov-report=term-missing
    ```
    Quel est le pourcentage de couverture global ? Quelles lignes ne sont pas couvertes ?

30. Le test `test_list_all` vérifie `data["total"] == 9` (3+3+3). Expliquez pourquoi ce total est 9 et pas 23195 (le total des vraies données). En quoi cela illustre-t-il l'isolation des tests ?

31. `test_search_too_short` vérifie le code HTTP `422`. D'où vient ce comportement ? (indice : inspectez `SearchRequest` dans `app/models.py`). Quel mécanisme Pydantic génère automatiquement cette validation ?

32. Le test `test_pagination` vérifie que `len(data["data"]) == 2` mais `data["total"] == 3`. Expliquez la distinction entre le nombre d'éléments retournés et le total. Pourquoi cette distinction est-elle importante côté frontend ?

### 3.3 Écrire de nouveaux tests

**Questions :**

33. Écrivez un test `test_search_no_results` qui vérifie que la recherche avec le mot `"xyzxyzxyz"` retourne `total == 0` et une liste vide.

34. Écrivez un test `test_all_contains_three_types` qui vérifie que la réponse de `GET /api/v1/all` contient au moins un enregistrement de chaque type (`naf`, `rome`, `matching`).

35. Proposez un scénario de test pour l'endpoint `GET /api/v1/mapping/naf-to-rome/{code_naf}` avec un code NAF qui **n'existe pas dans les correspondances** (mais qui existe dans les NAF). Quel comportement attendez-vous ? Écrivez le test.

---

## Partie 4 — CI/CD avec GitHub Actions

> Objectif : comprendre comment automatiser les vérifications de qualité à chaque commit.

### 4.1 Lire un pipeline CI/CD

Ouvrez `.github/workflows/ci.yml`.

**Questions :**

36. Sur quels événements Git le pipeline se déclenche-t-il (`on:`) ? Quelle est la différence entre un trigger sur `push` et sur `pull_request` ?
37. Combien de jobs le pipeline contient-il ? Listez-les et décrivez leur rôle.
38. Qu'est-ce que `needs:` dans un job GitHub Actions ? Pourquoi le job `build` dépend-il du job `test` ?
39. Le job de build publie une image sur GHCR (GitHub Container Registry). Quelle est la différence entre GHCR et Docker Hub ? Pourquoi préférer GHCR pour un projet hébergé sur GitHub ?

### 4.2 Le pipeline en pratique

**Questions :**

40. Si un test échoue sur une Pull Request, que se passe-t-il ? Le merge est-il bloqué automatiquement ?
41. Le pipeline utilise `docker/build-push-action`. Expliquez la différence entre `push: true` (publication) et `push: false` (build seul). Dans quel contexte utilise-t-on chaque option ?
42. Qu'est-ce que le cache Docker dans GitHub Actions (`cache-from`, `cache-to`) ? Quel temps cela fait-il gagner sur un pipeline typique ?
43. Vous souhaitez ajouter une étape de **linting** (vérification du style de code avec `ruff`) avant les tests. Ajoutez ce job au pipeline. Assurez-vous que les tests ne tournent que si le linting passe.

### 4.3 Concepts DevOps

**Questions :**

44. Définissez en vos mots : **CI (Continuous Integration)**, **CD (Continuous Delivery)** et **CD (Continuous Deployment)**. Quelle est la différence entre Delivery et Deployment ?
45. Dans une pipeline CI/CD mature, on parle de "shift left" (déplacer les vérifications vers la gauche de la chaîne). Expliquez ce principe en lien avec notre pipeline.
46. Qu'est-ce qu'un **artefact** dans un pipeline CI/CD ? Dans notre cas, quel est l'artefact produit et où est-il stocké ?

---

## Partie 5 — Observabilité et production

> Objectif : comprendre comment surveiller une API en production grâce aux mécanismes intégrés.

### 5.1 Healthcheck

**Questions :**

47. Lancez `docker inspect naf_rome_api` et trouvez la section `"Health"`. Quel est l'état actuel (`Status`) ? Combien de vérifications ont été effectuées ?
48. L'endpoint `/health` retourne un JSON. Quels champs contient-il ? Pourquoi un endpoint de santé doit-il être **léger** (réponse rapide, pas de dépendance aux données) ?
49. Dans `docker-compose.yml`, le service `api` dépend de `redis` avec `condition: service_healthy`. Que se passe-t-il si Redis ne démarre pas ? Simulez ce cas en commentant le service redis et en relançant.

### 5.2 Logs et métriques

**Questions :**

50. Lancez `docker compose logs api` puis `docker compose logs -f api`. Quelle est la différence ? Identifiez une ligne de log au format structuré (JSON) produite par `structlog`.
51. Accédez à http://localhost:8000/metrics. Quel format de données reconnaissez-vous ? Quel outil standard de monitoring utilise ce format ?
52. Quels compteurs sont exposés par `/metrics` ? Identifiez au moins 3 métriques et expliquez ce qu'elles mesurent.

### 5.3 Politiques de redémarrage

**Questions :**

53. Le docker-compose.yml définit `restart: unless-stopped` pour l'API. Quelles sont les 4 valeurs possibles de `restart` ? Dans quel contexte de déploiement `restart: always` est-il préférable ?
54. Simulez un crash de l'API avec `docker compose exec api kill 1`. Que se passe-t-il ? Docker redémarre-t-il le conteneur automatiquement ? Combien de temps cela prend-il ?

### 5.4 Sécurité des conteneurs

**Questions :**

55. Le Dockerfile crée un utilisateur `appuser` avec UID 1001. Vérifiez avec `docker compose exec api whoami`. Pourquoi est-il dangereux de faire tourner une application en tant que `root` dans un conteneur ?
56. Le volume de données est monté en `:ro` (read-only). Testez en lançant `docker compose exec api touch /app/data/test.txt`. Que se passe-t-il ? Quel risque sécurité cela prévient-il ?

---

## Rendu attendu

Votre document de rendu doit contenir :

- [ ] Les réponses aux **56 questions** numérotées
- [ ] Les **2 tests** écrits (questions 33 et 34)
- [ ] Le **job de linting** ajouté au pipeline CI (question 43)
- [ ] Au minimum **8 captures d'écran** annotées :
  - `docker images` montrant la taille de l'image
  - `docker ps` avec les conteneurs actifs
  - Le résultat de `docker build --target test .`
  - La sortie de `pytest --cov=app --cov-report=term-missing`
  - L'endpoint `/metrics` dans le navigateur
  - La section Health de `docker inspect`
  - Une exécution du pipeline GitHub Actions (succès)
  - Un exemple de `docker compose logs -f api` avec des logs structurés
- [ ] Une **conclusion personnelle** (15-20 lignes) : qu'est-ce que Docker change concrètement dans votre façon de livrer du code ? Qu'avez-vous trouvé le plus complexe ? Le plus utile ?

---

## Ressources

| Ressource | URL |
|---|---|
| Documentation Docker | https://docs.docker.com/ |
| Best practices Dockerfile | https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ |
| Docker Compose reference | https://docs.docker.com/compose/compose-file/ |
| GitHub Actions documentation | https://docs.github.com/en/actions |
| GHCR (GitHub Container Registry) | https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry |
| pytest documentation | https://docs.pytest.org/ |
| Prometheus metrics format | https://prometheus.io/docs/concepts/data_model/ |

---

*Évaluation conçue dans le cadre du Master IA · CreativeTech — TP 1.2 Docker & CI/CD NAF-ROME*
