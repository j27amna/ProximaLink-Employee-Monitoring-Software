# views/__init__.py

from flask import Flask, send_from_directory
import os

app = Flask(__name__)
app.config.from_pyfile("../config.py")

# Register blueprints
from views import auth, dashboard, api

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp, url_prefix="/dashboard")
app.register_blueprint(api.bp, url_prefix="/api")


@app.route("/")
def index():
    return "Welcome to SecureTrack!"


@app.after_request
def add_cache_control_header(response):
    if "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/static/<path:filename>")
def serve_static(filename):
    response = send_from_directory(os.path.join(app.root_path, "static"), filename)
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    if "Server" in response.headers:
        response.headers["Server"] = "SecureTrack"
    return response


if __name__ == "__main__":
    app.run(debug=True)
