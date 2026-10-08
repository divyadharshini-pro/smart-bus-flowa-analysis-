from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "smartbusflow_secret_key"

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

# Bus details
BUSES = [
    {
        "bus_number": "TN-30-AB-1001",
        "driver": "Driver 1",
        "phone": "9876543210",
        "route": "Salem - Hosur",
        "start": "Salem",
        "destination": "Hosur",
        "latitude": 11.6643,
        "longitude": 78.1460,
        "speed": 0,
        "status": "Offline"
    },
    {
        "bus_number": "TN-30-AB-1002",
        "driver": "Driver 2",
        "phone": "9876543211",
        "route": "Salem - Bengaluru",
        "start": "Salem",
        "destination": "Bengaluru",
        "latitude": 11.6643,
        "longitude": 78.1460,
        "speed": 0,
        "status": "Offline"
    }
]


@app.route("/")
def login():
    return render_template("login.html")


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

        if user["role"] == "driver":
            return redirect(url_for("driver"))

    return render_template(
        "login.html",
        error="Invalid username or password"
    )


@app.route("/admin")
def admin():

    if session.get("role") != "admin":
        return redirect(url_for("login"))

    return render_template(
        "admin.html",
        username=session.get("username"),
        buses=BUSES
    )


@app.route("/driver")
def driver():

    if session.get("role") != "driver":
        return redirect(url_for("login"))

    return render_template(
        "driver.html",
        username=session.get("username"),
        buses=BUSES
    )


@app.route("/tracking")
def tracking():
    return render_template("tracking.html", buses=BUSES)


# -------------------------
# ADD BUS
# -------------------------

@app.route("/add_bus", methods=["POST"])
def add_bus():

    bus = {
        "bus_number": request.form.get("bus_number"),
       
