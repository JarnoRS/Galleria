import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
import config
import db
import images

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_images = images.get_images()
    return render_template("index.html", images=all_images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = images.get_image(image_id)
    return render_template("show_image.html", image=image)

@app.route("/add_image")
def add_image():
    return render_template("add_image.html")

@app.route("/edit_image/<int:image_id>")
def edit_image(image_id):
    image = images.get_image(image_id)
    if image["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_image.html", image=image)

@app.route("/update_image", methods=["POST"])
def update_image():
    image_id = request.form["image_id"]
    title = request.form["title"]
    kuvaus = request.form["description"]
    genre = request.form["genre"]
    image = images.get_image(image_id)
    if image["user_id"] != session["user_id"]:
        abort(403)

    images.update_image(image_id, title, kuvaus, genre)
    return redirect("/image/" + str(image_id))

@app.route("/delete_image/<int:image_id>", methods=["GET", "POST"])
def delete_image(image_id):
    if request.method == "GET":
        image = images.get_image(image_id)
        if image["user_id"] != session["user_id"]:
            abort(403)
        return render_template("delete_image.html", image=image)
    
    if request.method == "POST":
        if "remove" in request.form:
            images.delete_image(image_id)
            return redirect("/")
        else:
            return redirect("/image/" + str(image_id))

@app.route("/find_image")
def find_image():
    query = request.args.get("query")
    genre_query = request.args.getlist("genre")
    if query and not genre_query:
        results = images.find_images(query, None)
    elif genre_query and not query:
        results = images.find_images(None, genre_query)
    elif query and genre_query:
        results = images.find_images(query, genre_query)
    else:
        query = ""
        results= []
    return render_template("find_image.html", query=query, genre_query=genre_query,results=results)

@app.route("/create_image", methods=["POST"])
def create_image():
    title = request.form["title"]
    kuvaus = request.form["description"]
    genre = request.form["genre"]
    user_id = session["user_id"]
    date_added = date.today()

    images.add_image(title, kuvaus, genre, user_id, date_added)
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")