from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import gunicorn
import mysql.connector

app = Flask(__name__)

app.secret_key = "abcdefg"

session.permanent = False

db = mysql.connector.connect(
    host="us-cdbr-east-04.cleardb.com",
    user="b8601831567355",
    password="40a53098",
    database="heroku_008b3dac9b6fd1b"
)

cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS gradusers (id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), password VARCHAR(50))")

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html", message="")

@app.route('/login', methods=["POST","GET"])
def login():
    return render_template("login.html")

@app.route('/signup', methods=["POST", "GET"])
def signin():
    return render_template("signup.html", message="")

@app.route('/home', methods=["POST", "GET"])
def home():
    if "user" in session:
        name = session["user"]

        return render_template("home.html", username=name)

    else:
        return render_template("index.html")


@app.route('/signuproute', methods=["POST", "GET"])
def signuproute():

    if request.method == "POST":
        name = request.form["username"]
        if (name == ""):
            return render_template("signup.html", message="No username entered")
        if (len(name) > 50):
            return render_template("signup.html", message="Username too long")

        password = request.form["password"]
        if (password == ""):
            return render_template("signup.html", message="No password entered")
        if (len(password) > 50):
            return render_template("signup.html", message="Password too long")

        sql = "SELECT * FROM gradusers WHERE username=%s"
        cursor.execute(sql, (name,))
        derp = cursor.fetchone()
        if (derp != None):
            return render_template("signup.html", message="Username already taken")

        sql = "INSERT INTO gradusers(username, password) VALUES (%s, %s)"
        cursor.execute(sql, (name, password))
        db.commit()

        session["user"] = name
        return redirect(url_for("home"))
    else:
        return render_template("signup.html", message="")


@app.route('/loginroute', methods=["POST", "GET"])
def loginroute():

    if request.method == "POST":
        name = request.form["username"]
        name = request.form["username"]
        if (name == ""):
            return render_template("login.html", message="No username entered")
        if (len(name) > 50):
            return render_template("login.html", message="Username too long")

        password = request.form["password"]
        if (password == ""):
            return render_template("login.html", message="No password entered")
        if (len(password) > 50):
            return render_template("login.html", message="Password too long")

        sql = "SELECT * FROM gradusers WHERE username=%s"

        cursor.execute(sql, (name,))

        shouldbe = cursor.fetchone()

        if shouldbe is None:
            return render_template("login.html", message="Account Doesn't Exist, Please Create a New One")

        if str(password) == shouldbe[2]:
            session["user"] = name
            return redirect(url_for("home", message="Just logged in"))

        else:
            return render_template("login.html", message="Incorrect Password")

    else:
        return render_template("login.html")

@app.route('/logout', methods=["POST", "GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()

