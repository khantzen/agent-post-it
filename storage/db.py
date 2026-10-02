import os
import sqlite3

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
