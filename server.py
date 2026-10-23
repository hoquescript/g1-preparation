#!/usr/bin/env python3
"""Serve quiz.html locally and keep answer history in g1_history.db (SQLite).

Usage: python3 server.py [port]   then open http://127.0.0.1:8000/
"""
import json
import sqlite3
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "g1_history.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS attempts (
    id          INTEGER PRIMARY KEY,
    question    INTEGER NOT NULL,
    picked      TEXT    NOT NULL,
    answer      TEXT    NOT NULL,
    is_correct  INTEGER NOT NULL,
    mode        TEXT    NOT NULL,
    answered_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
CREATE INDEX IF NOT EXISTS attempts_question ON attempts(question);
"""


def connect():
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    return conn


def stats():
    with connect() as conn:
        rows = conn.execute(
            "SELECT question, SUM(is_correct), SUM(1 - is_correct) FROM attempts GROUP BY question"
        ).fetchall()
    return {n: {"right": right, "wrong": wrong} for n, right, wrong in rows}


def record(body):
    picked, answer = str(body["picked"]), str(body["answer"])
    with connect() as conn:
        conn.execute(
            "INSERT INTO attempts (question, picked, answer, is_correct, mode) VALUES (?, ?, ?, ?, ?)",
            (int(body["n"]), picked, answer, int(picked == answer), str(body["mode"])),
        )


def reset():
    with connect() as conn:
        conn.execute("DELETE FROM attempts")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, data, status=200):
        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/stats":
            return self.send_json(stats())
        if self.path == "/":
            self.path = "/quiz.html"
        if not self.path.split("?")[0].endswith((".html", ".js")):
            return self.send_error(404)
        super().do_GET()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(length) or b"{}")
            if self.path == "/api/answer":
                record(body)
            elif self.path == "/api/reset":
                reset()
            else:
                return self.send_error(404)
        except (ValueError, KeyError, TypeError) as e:
            return self.send_json({"error": str(e)}, 400)
        self.send_json({"ok": True})


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    connect().close()
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"G1 quiz at http://127.0.0.1:{port}/  (history in {DB.name})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
