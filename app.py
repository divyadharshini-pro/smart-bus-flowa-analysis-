from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "smartbusflow_secret_key"


# -----------------------------
# Demo login credentials
# -----------------------------
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "driver": {
        "password": "driver123",
        "role": "driver"
    }
}


# -----------------------------
# Home / Login
# -----------------------------
@app.route("/")
def login():
    return render_template("login.html")


# -----------------------------
# Login Authentication
# -----------------------------
@app.route("/login", methods=["POST"])
def do_login():

    username = request.form.get("username")
    password = request.form.get("password")

    user = USERS.get(username)

    if user and user["password"] == password:

        session["username"] = username
        session["role"] = user["role"]

        if user["role"] == "admin":
            return redirect(url_for("admin"))

        elif user["role"] == "driver":
            return redirect(url_for("driver"))

    return render_template(
        "login.html",
        error="Invalid username or password"
    )


# -----------------------------
# Admin Dashboard
# -----------------------------
@app.route("/admin")
def admin():

    if session.get("role") != "admin":
        return redirect(url_for("login"))

    return render_template(
        "admin.html",
        username=session.get("username")
    )


# -----------------------------
# Driver Dashboard
# -----------------------------
@app.route("/driver")
def driver():

    if session.get("role") != "driver":
        return redirect(url_for("login"))

    return render_template(
        "driver.html",
        username=session.get("username")
    )


# -----------------------------
# Bus Tracking Page
# -----------------------------
@app.route("/tracking")
def tracking():

    return render_template("tracking.html")


# -----------------------------
# GPS Location API
# -----------------------------
@app.route("/update_location", methods=["POST"])
def update_location():

    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # Demo response
    return jsonify({
        "status": "success",
        "latitude": latitude,
        "longitude": longitude
    })


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
