from flask import Flask, render_template, request, redirect
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="05230523",
    database="froshimsDB"
)

cursor = conn.cursor(dictionary=True)

app = Flask(__name__)

SPORTS = ["Basketball", "Soccer", "Ultimate Frisbee"]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if id:
        cursor.execute("DELETE FROM registrants WHERE id = (%s)", (id, ))
        conn.commit()
    return redirect("/registrants")

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing Name")

    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing Sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid Sport")

    cursor.execute("INSERT INTO registrants (name, sport) VALUES (%s, %s)", (name, sport))
    conn.commit()
    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    cursor.execute("SELECT * FROM registrants")
    registrants = cursor.fetchall()
    return render_template("registrants.html", registrants=registrants)