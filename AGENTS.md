# My Post It

Application de gestion de post-its en Python/Flask.

Chaque post-it est lie a un ou plusieurs projets (champ `project`, noms separes par `|`).

## Structure du code

- `app.py` : routes HTTP, validation des requetes et reponses. Aucune logique metier ni SQL direct
- `postit/postit.py` : logique metier des post-its (create/get/update/delete/list), appelle `storage/db.py`
- `storage/db.py` : acces SQLite (init_db, fetch_one, fetch_all, insert, execute)
- `api_description.agents.json` : description de l'API servie par le endpoint `/agents`
- `templates/` : page HTML de gestion

## Lancement

- En local : `nix-shell --run "flask --app app run"` (defaut : `127.0.0.1:5000`, reglable via `FLASK_RUN_HOST` et `FLASK_RUN_PORT`)
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

- Stockage en base SQLite Locale
- `PUT` ne permet pas de modifier le champ `project` (fixe a la creation)
- Mode debug desactive par defaut ; activable via `FLASK_DEBUG=1` (usage local uniquement)
- Projet locale à ne pas utiliser en production
