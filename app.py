import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
import config
import db
import images
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_images = images.get_images()
    return render_template("index.html", images=all_images)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    images = users.get_users_images(user_id)
    comments = users.get_user_comments(user_id)[:3]
    return render_template("show_user.html", user=user, images=images, comments=comments)

@app.route("/image/<int:image_id>", methods=["GET", "POST"])
def show_image(image_id):
    image = images.get_image(image_id)
    comments = images.get_comments(image_id)
    grade_mean = images.get_grades(image_id)
    if not image:
        abort(404)
    return render_template("show_image.html", image=image, comments=comments, grade_mean=grade_mean)

@app.route("/add_comment/<int:image_id>", methods=["POST"])
def add_comment(image_id):
    require_login()
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if "user_id" in session:
        image_id = request.form["image_id"]
        comment = request.form["comment"]
        user_id = session["user_id"]
        date_added = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        image_title = image["title"]
        images.add_comment(image_id, comment, user_id, date_added, image_title)
    comments = images.get_comments(image_id)
    grade_mean = images.get_grades(image_id)
    return redirect("/image/" + str(image_id))

@app.route("/add_grade/<int:image_id>", methods=["POST"])
def add_grade(image_id):
    require_login()
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if "user_id" in session:
        image_id = image["id"]
        grade = request.form["grade"]
        user_id = session["user_id"]
        if grade:
            images.add_grade(image_id, user_id, grade)
    comments = images.get_comments(image_id)
    grade_mean = images.get_grades(image_id)
    return redirect("/image/" + str(image_id))

@app.route("/add_image")
def add_image():
    require_login()
    classes = images.get_classes()
    return render_template("add_image.html", classes=classes)

@app.route("/edit_image/<int:image_id>")
def edit_image(image_id):
    require_login()
    classes = images.get_classes()
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if image["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_image.html", image=image, classes=classes)

@app.route("/update_image", methods=["POST"])
def update_image():
    require_login()
    image_id = request.form["image_id"]
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    kuvaus = request.form["description"]
    if len(kuvaus) > 1000:
        abort(403)
    genre = request.form["genre"]
    classes = images.get_classes()
    if genre not in classes["genre"]:
        abort(403)
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if image["user_id"] != session["user_id"]:
        abort(403)

    images.update_image(image_id, title, kuvaus, genre)
    return redirect("/image/" + str(image_id))

@app.route("/delete_image/<int:image_id>", methods=["GET", "POST"])
def delete_image(image_id):
    require_login()
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if image["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
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
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    kuvaus = request.form["description"]
    if len(kuvaus) > 1000:
        abort(403)
    genre = request.form["genre"]
    classes = images.get_classes()
    if genre not in classes["genre"]:
        abort(403)
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
    kuvaus = request.form["kuvaus"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"  
    try:
        users.create_user(username, password1, kuvaus)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return render_template("user_created.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")