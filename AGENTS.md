# My Post It

Application de gestion de post-its en Python/Flask.

Chaque post-it est lie a un ou plusieurs projets (champ `project`, noms separes par `|`).

## Lancement

- En local : `nix-shell --run "python app.py"` (port 5000)
- En conteneur : `docker compose up -d` (image `local/kha-post-it:1.0.0`, port 5000)

## API

Le descriptif complet de l'API est disponible en JSON sur `http://localhost:5000/agents`.

Endpoints principaux :

- `POST /api/postit` : cree un post-it (`title`, `body`, `project`, tous requis)
- `GET /api/postit/<id>` : retourne le post-it
- `PUT /api/postit/<id>` : modifie `title` et `body`
- `DELETE /api/postit/<id>` : supprime le post-it
- `GET /api/postit/list/?sort=desc|asc&projet=<nom>` : liste les post-its tries par date (defaut : du plus recent au plus ancien), filtrable par projet
- `GET /` : page HTML de gestion des post-its

## Remarques

- Stockage en memoire : les post-its sont perdus au redemarrage
- `PUT` ne permet pas de modifier le champ `project` (fixe a la creation)
- `debug=True` est actif dans `app.py` : a desactiver si l'application est exposee au-dela du poste local
