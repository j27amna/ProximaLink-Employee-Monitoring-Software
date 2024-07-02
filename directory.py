# directory.py
import os

BASE_DIR = "LoggedData"


def setup_user_directories(username):
    user_dir = os.path.join(BASE_DIR, username)
    clipboard_dir = os.path.join(user_dir, "Clipboard")
    screenshot_dir = os.path.join(user_dir, "Screenshot")
    files_dir = os.path.join(user_dir, "Files")
    video_dir = os.path.join(user_dir, "Video")

    os.makedirs(clipboard_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(files_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)

    return user_dir, clipboard_dir, screenshot_dir, files_dir, video_dir
