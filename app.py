import json
import os

from flask import Flask, jsonify, render_template, request

from postit import postit
from storage import db

app = Flask(__name__)

API_DESCRIPTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_description.agents.json")

db.init_db()


def error(message, status):
    return jsonify({"error": message}), status


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
    if not isinstance(project, str) or not postit.normalize_project(project):
        return error("Champ 'project' requis (chaine non vide, projets separes par '|')", 400)

    created = postit.create(title, body, postit.normalize_project(project))
    return jsonify(created), 201


@app.route("/api/postit/<int:postit_id>", methods=["GET"])
def get_postit(postit_id):
    result = postit.get(postit_id)
    if result is None:
        return error("Post-it introuvable", 404)
    return jsonify(result)


@app.route("/api/postit/<int:postit_id>", methods=["DELETE"])
def delete_postit(postit_id):
    if not postit.delete(postit_id):
        return error("Post-it introuvable", 404)
    return "", 204


@app.route("/api/postit/<int:postit_id>", methods=["PUT"])
def update_postit(postit_id):
    if postit.get(postit_id) is None:
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

    return jsonify(postit.update(postit_id, title, body))


@app.route("/api/postit/list/", methods=["GET"])
def list_postits():
    sort = request.args.get("sort", "desc")
    if sort not in ("asc", "desc"):
        return error("Parametre 'sort' invalide : valeurs possibles 'asc', 'desc'", 400)

    project = request.args.get("projet", "").strip()
    return jsonify(postit.list_all(sort, project))


@app.route("/agents", methods=["GET"])
def agents():
    with open(API_DESCRIPTION_PATH, encoding="utf-8") as description_file:
        return jsonify(json.load(description_file))
