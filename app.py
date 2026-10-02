import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DB_PATH = os.environ.get("POSTIT_DB", "postits.db")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS postits ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, "
            "body TEXT NOT NULL, "
            "project TEXT NOT NULL, "
            "created_at TEXT NOT NULL)"
        )


def postit_from_row(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "body": row["body"],
        "project": row["project"],
        "created_at": row["created_at"],
    }


def fetch_one(sql, params=()):
    with db() as conn:
        return conn.execute(sql, params).fetchone()


def fetch_all(sql, params=()):
    with db() as conn:
        return conn.execute(sql, params).fetchall()


def insert(sql, params=()):
    with db() as conn:
        cursor = conn.execute(sql, params)
        return cursor.lastrowid


def execute(sql, params=()):
    with db() as conn:
        cursor = conn.execute(sql, params)
        return cursor.rowcount


def error(message, status):
    return jsonify({"error": message}), status


def normalize_project(value):
    projects = [p.strip() for p in value.split("|")]
    return "|".join(p for p in projects if p)


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/postit", methods=["POST"])
def create_postit():
    data = request.get_json(silent=True)
    if data is None:
        return error("Corps JSON requis", 400)

    title = data.get("title")
    body = data.get("body")
    project = data.get("project")
    if not isinstance(title, str) or not title.strip():
        return error("Champ 'title' requis (chaine non vide)", 400)
    if not isinstance(body, str) or not body.strip():
        return error("Champ 'body' requis (chaine non vide)", 400)
    if not isinstance(project, str) or not normalize_project(project):
        return error("Champ 'project' requis (chaine non vide, projets separes par '|')", 400)

    project = normalize_project(project)
    created_at = datetime.now(timezone.utc).isoformat()
    postit_id = insert(
        "INSERT INTO postits (title, body, project, created_at) VALUES (?, ?, ?, ?)",
        (title, body, project, created_at),
    )
    return jsonify({"id": postit_id, "title": title, "body": body, "project": project, "created_at": created_at}), 201


@app.route("/api/postit/<int:postit_id>", methods=["GET"])
def get_postit(postit_id):
    row = fetch_one("SELECT * FROM postits WHERE id = ?", (postit_id,))
    if row is None:
        return error("Post-it introuvable", 404)
    return jsonify(postit_from_row(row))


@app.route("/api/postit/<int:postit_id>", methods=["DELETE"])
def delete_postit(postit_id):
    deleted = execute("DELETE FROM postits WHERE id = ?", (postit_id,))
    if deleted == 0:
        return error("Post-it introuvable", 404)
    return "", 204


@app.route("/api/postit/<int:postit_id>", methods=["PUT"])
def update_postit(postit_id):
    row = fetch_one("SELECT * FROM postits WHERE id = ?", (postit_id,))
    if row is None:
        return error("Post-it introuvable", 404)

    data = request.get_json(silent=True)
    if data is None:
        return error("Corps JSON requis", 400)

    title = data.get("title")
    body = data.get("body")
    if not isinstance(title, str) or not title.strip():
        return error("Champ 'title' requis (chaine non vide)", 400)
    if not isinstance(body, str) or not body.strip():
        return error("Champ 'body' requis (chaine non vide)", 400)

    execute("UPDATE postits SET title = ?, body = ? WHERE id = ?", (title, body, postit_id))
    return jsonify(postit_from_row(fetch_one("SELECT * FROM postits WHERE id = ?", (postit_id,))))


@app.route("/api/postit/list/", methods=["GET"])
def list_postits():
    sort = request.args.get("sort", "desc")
    if sort not in ("asc", "desc"):
        return error("Parametre 'sort' invalide : valeurs possibles 'asc', 'desc'", 400)

    result = [postit_from_row(row) for row in fetch_all("SELECT * FROM postits")]
    result = sorted(result, key=lambda p: p["created_at"], reverse=sort == "desc")

    project = request.args.get("projet", "").strip()
    if project:
        result = [p for p in result if project in p["project"].split("|")]
    return jsonify(result)


@app.route("/agents", methods=["GET"])
def agents():
    return jsonify({
        "name": "My Post It",
        "description": "API de gestion de post-its",
        "base_url": "http://localhost:5000",
        "concepts": {
            "project": "Chaque post-it est lie a un ou plusieurs projets, "
                       "stockes dans le champ 'project' sous forme d'une chaine "
                       "avec les noms separes par '|' (ex: 'web|infra').",
        },
        "endpoints": [
            {
                "method": "POST",
                "path": "/api/postit",
                "description": "Cree un post-it lie a un ou plusieurs projets",
                "body": {
                    "title": "string (requis)",
                    "body": "string (requis)",
                    "project": "string (requis) : nom(s) de(s) projet(s), separes par '|' (ex: 'web|infra')",
                },
                "returns": "Le post-it cree avec son champ 'project' (201)",
            },
            {
                "method": "GET",
                "path": "/api/postit/<id>",
                "description": "Retourne le post-it correspondant a l'id",
                "returns": "Le post-it (200) ou 404",
            },
            {
                "method": "DELETE",
                "path": "/api/postit/<id>",
                "description": "Supprime le post-it correspondant a l'id",
                "returns": "204 ou 404",
            },
            {
                "method": "PUT",
                "path": "/api/postit/<id>",
                "description": "Modifie le titre et le body du post-it correspondant a l'id",
                "body": {"title": "string (requis)", "body": "string (requis)"},
                "returns": "Le post-it modifie (200) ou 404",
            },
            {
                "method": "GET",
                "path": "/api/postit/list/",
                "description": "Liste tous les post-its tries par date de creation",
                "query": {
                    "sort": "asc|desc (optionnel, defaut: desc, du plus recent au plus ancien)",
                    "projet": "string (optionnel) : ne retourne que les post-its lies a ce projet (correspondance exacte sur le nom du projet)",
                },
                "returns": "Liste des post-its (200)",
            },
        ],
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
