from datetime import datetime, timezone

from storage import db


def normalize_project(value):
    projects = [p.strip() for p in value.split("|")]
    return "|".join(p for p in projects if p)


def from_row(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "body": row["body"],
        "project": row["project"],
        "created_at": row["created_at"],
    }


def create(title, body, project):
    created_at = datetime.now(timezone.utc).isoformat()
    postit_id = db.insert(
        "INSERT INTO postits (title, body, project, created_at) VALUES (?, ?, ?, ?)",
        (title, body, project, created_at),
    )
    return {"id": postit_id, "title": title, "body": body, "project": project, "created_at": created_at}


def get(postit_id):
    row = db.fetch_one("SELECT * FROM postits WHERE id = ?", (postit_id,))
    if row is None:
        return None
    return from_row(row)


def update(postit_id, title, body):
    updated = db.execute("UPDATE postits SET title = ?, body = ? WHERE id = ?", (title, body, postit_id))
    if updated == 0:
        return None
    return get(postit_id)


def delete(postit_id):
    return db.execute("DELETE FROM postits WHERE id = ?", (postit_id,)) > 0


def list_all(sort, project):
    order = "ASC" if sort == "asc" else "DESC"
    result = [from_row(row) for row in db.fetch_all("SELECT * FROM postits ORDER BY created_at " + order)]
    if not project:
        return result
    return [p for p in result if project in p["project"].split("|")]
