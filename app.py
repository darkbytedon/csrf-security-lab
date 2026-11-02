
from flask import Flask, request, session, redirect, url_for, render_template_string
import secrets

app = Flask(__name__)
app.secret_key = "local-training-secret-key"

users = {
    "alice": {
        "password": "alice123",
        "email": "alice@example.com"
    }
}

PAGE = """
<h1>Account Settings</h1>

{% if username %}
    <p>Logged in as: {{ username }}</p>
    <p>Current email: {{ email }}</p>

    <form method="POST" action="/change-email">
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
        <label>New email:</label>
        <input type="email" name="email" required>
        <button type="submit">Change Email</button>
    </form>

    <p><a href="/logout">Logout</a></p>
{% else %}
    <h2>Login</h2>
    <form method="POST" action="/login">
        <input name="username" placeholder="Username" required>
        <input name="password" type="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
{% endif %}

<p>{{ message }}</p>
"""

@app.route("/")
def home():
    username = session.get("username")
    email = users[username]["email"] if username else None

    if username:
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        csrf_token = session["csrf_token"]
    else:
        csrf_token = ""

    return render_template_string(
        PAGE,
        username=username,
        email=email,
        csrf_token=csrf_token,
        message=request.args.get("message", "")
    )

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username]["password"] == password:
        session.clear()
        session["username"] = username
        session["csrf_token"] = secrets.token_urlsafe(32)
        return redirect(url_for("home"))

    return "Invalid login", 401

@app.route("/change-email", methods=["POST"])
def change_email():
    username = session.get("username")

    if not username:
        return "Login required", 401

    submitted_token = request.form.get("csrf_token", "")
    session_token = session.get("csrf_token", "")

    if not session_token or not secrets.compare_digest(
        submitted_token, session_token
    ):
        return "CSRF validation failed", 403

    new_email = request.form.get("email", "")

    if "@" not in new_email:
        return "Invalid email", 400

    users[username]["email"] = new_email

    return redirect(url_for("home", message="Email updated successfully"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=False)
