# Agents Post It App

Application de gestion de post-its en Python/Flask, pensée pour être utilisée par un agent de code (CLI type Vibe) via son API HTTP. Chaque post-it est lié à un ou plusieurs projets (champ `project`, noms séparés par `|`), ce qui permet à l'agent de retrouver les notes associées au dépôt sur lequel il travaille.

Points clés :

- API HTTP sur le port 5000, descriptif complet sur `http://localhost:5000/agents`
- Page HTML de gestion sur `http://localhost:5000/`
- Stockage SQLite : base `postits.db` (chemin surchargeable via la variable d'environnement `POSTIT_DB`), les post-its persistent au redémarrage

## How to

Build de l'image et lancement via docker compose :

```bash
docker compose up -d --build
```

L'application est ensuite disponible sur `http://localhost:5000`. Les post-its sont persistés dans le volume Docker `postit-data` (fichier `/app/data/postits.db` dans le conteneur), ils survivent aux recréations du conteneur.

Pour un usage local sans conteneur :

```bash
nix-shell --run "python app.py"
```

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
