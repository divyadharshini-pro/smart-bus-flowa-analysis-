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
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = USERS.get(username)

    if user and user["password"] == password:
        session["username"] = username
        session["role"] = user["role"]

        if user["role"] == "admin":
            return redirect(url_for("admin"))

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
    return render_template(
        "tracking.html",
        buses=BUSES
    )


@app.route("/add_bus", methods=["POST"])
def add_bus():

    bus_number = request.form.get(
        "bus_number", ""
    ).strip()

    driver_name = request.form.get(
        "driver", ""
    ).strip()

    phone = request.form.get(
        "phone", ""
    ).strip()

    route = request.form.get(
        "route", ""
    ).strip()

    start = request.form.get(
        "start", ""
    ).strip()

    destination = request.form.get(
        "destination", ""
    ).strip()

    if not all([
        bus_number,
        driver_name,
        phone,
        route,
        start,
        destination
    ]):
        return "All bus details are required.", 400

    for bus in BUSES:
        if bus["bus_number"].lower() == bus_number.lower():
            return "Bus number already exists.", 400

    BUSES.append({
        "bus_number": bus_number,
        "driver": driver_name,
        "phone": phone,
        "route": route,
        "start": start,
        "destination": destination,
        "latitude": 0,
        "longitude": 0,
        "speed": 0,
        "status": "Offline"
    })

    return redirect(url_for("admin"))


@app.route("/search_bus")
def search_bus():

    query = request.args.get(
        "q", ""
    ).strip().lower()

    if not query:
        return jsonify(BUSES)

    results = []

    for bus in BUSES:

        if (
            query in bus["bus_number"].lower()
            or query in bus["driver"].lower()
            or query in bus["route"].lower()
        ):
            results.append(bus)

    return jsonify(results)


@app.route("/api/buses")
def get_buses():
    return jsonify(BUSES)


@app.route("/update_location", methods=["POST"])
def update_location():

    data = request.get_json(
        silent=True
    ) or {}

    bus_number = str(
        data.get("bus_number", "")
    ).strip()

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    speed = data.get("speed", 0)

    if not bus_number:
        return jsonify({
            "status": "error",
            "message": "Bus number is required"
        }), 400

    for bus in BUSES:

        if bus["bus_number"] == bus_number:

            bus["latitude"] = latitude
            bus["longitude"] = longitude
            bus["speed"] = speed
            bus["status"] = "Live"

            return jsonify({
                "status": "success",
                "message": "Location updated",
                "bus": bus
            })

    return jsonify({
        "status": "error",
        "message": "Bus not found"
    }), 404


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
        )
