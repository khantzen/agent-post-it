# Agents Post It App

Post-it management application in Python/Flask, designed to be used by a coding agent (CLI such as Vibe) through its HTTP API. Each post-it is linked to one or more projects (`project` field, names separated by `|`), which allows the agent to find the notes associated with the repository it is working on.

Key points:

- HTTP API on port 5000, full description at `http://localhost:5000/agents`
- HTML management page at `http://localhost:5000/`
- SQLite storage: `postits.db` database (path can be overridden via the `POSTIT_DB` environment variable), post-its persist across restarts
- Host, port and debug mode are controlled by the standard Flask environment variables: `FLASK_RUN_HOST`, `FLASK_RUN_PORT` and `FLASK_DEBUG` (debug disabled by default)

## How to

Build the image and start it via docker compose:

```bash
docker compose up -d --build
```

The application is then available at `http://localhost:5000`. Post-its are persisted in the `postit-data` Docker volume (`/app/data/postits.db` file inside the container), they survive container recreations.

For local usage without a container:

```bash
nix-shell --run "flask --app app run"
```

By default the app listens on `127.0.0.1:5000`. Override with `FLASK_RUN_HOST` and `FLASK_RUN_PORT`:

```bash
FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=5000 nix-shell --run "flask --app app run"
```

Debug mode is disabled by default; enable it with `FLASK_DEBUG=1` for local development only.

## Add it to your AGENTS.md

### 🇬🇧 English

```markdown
## POST-IT

- A post-it application is available on this machine, accessible via http api.
- You will find the details of the api endpoints at `http://localhost:5000/agents`
- If I ask you to add/remove/update/list/read a post-it, I'd like you to interact with this application
- Each post-it is linked to a project, here is how to define it by order of priority
  - I give you the project name
  - Name of the git repo you are in
  - Name of the folder you are in
```

### 🇫🇷 Français

```markdown
## POST-IT

- Une application de post it est disponible sur ce post elle est accessible via api http.
- Tu trouveras le détail des endpoints de l'api sur `http://localhost:5000/agents`
- Si je te demande de rajouter/supprimer/modifier/lister/lire un post-it j'aimerais que tu interagisses avec cette application
- Chaque post-it est lié à un projet, voici comment le définir par ordre de priorité
  - Je te donne le nom du projet
  - Nom du repo git dans lequel tu te trouves
  - Nom du dossier dans lequel tu te trouves
```
