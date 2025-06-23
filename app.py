import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, make_response
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
    sample_images = images.get_sample_images()
    return render_template("index.html", images=sample_images)

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    images = users.get_users_images(user_id)
    comments = users.get_user_comments(user_id) or []
    comments = comments[:3]
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
    image_description = request.form["description"]
    if len(image_description) > 1000:
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

    images.update_image(image_id, title, image_description, genre)
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
    image_description = request.form["description"]
    if len(image_description) > 1000:
        abort(403)
    genre = request.form["genre"]
    classes = images.get_classes()
    if genre not in classes["genre"]:
        abort(403)
    file = request.files["profile_pic"]
    if not file.filename.endswith(".jpg"):
        return "VIRHE: väärä tiedostomuoto"
    image = file.read()
    if len(image) > 1000 * 1024:
        return "VIRHE: liian suuri kuva"
    user_id = session["user_id"]
    date_added = date.today()
    images.add_image(title, image_description, genre, user_id, date_added, image)
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    user_description = request.form["description"]
    profile_pic = None
    file = request.files["profile_pic"]
    if file and file.filename:
        if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"
        profile_pic = file.read()
        if len(profile_pic) > 100 * 1024:
            return "VIRHE: liian suuri kuva"
    if len(password1) < 5:
        return "VIRHE: Salasanan pituuden tulee olla vähintään 5 merkkiä."
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"  
    try:
        users.create_user(username, password1, user_description, profile_pic)
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

@app.route("/edit_user/<int:user_id>")
def edit_user(user_id):
    require_login()
    user_id = session["user_id"]
    user = users.get_user(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
    require_login()
    user_id = session["user_id"]
    user = users.get_user(user_id)
    if request.method == "GET":
        return render_template("delete_user.html", user=user)
    if request.method == "POST":
        username = user["username"]
        password = request.form["password"] 
        user_id = users.check_login(username, password)
        if user_id:
            del session["user_id"]
            del session["username"]
            users.delete(user_id)
            return redirect("/")
        else:
            abort(403)

@app.route("/update_user", methods=["POST"])
def update_user():
    require_login()
    user_id = request.form["user_id"]
    file = request.files["image"]
    user_description = request.form["description"]
    if file:
        if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"
        image = file.read()
        if len(image) > 100 * 1024:
            return "VIRHE: liian suuri kuva"
        user_id = session["user_id"]
        if user_id != session["user_id"]:
            abort(403)
        users.update_profile(user_id, image, user_description)
        return redirect("/user/" + str(user_id))
    else:
        users.update_profile(user_id, None, user_description)
        return redirect("/user/" + str(user_id))

@app.route("/all_users")
def all_users():
    every_user = users.get_every_user()
    return render_template("all_users.html", every_user=every_user)

@app.route("/profile_pic/<int:user_id>")
def show_profile_pic(user_id):
    image = users.get_profile_pic(user_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/picture/<int:image_id>")
def show_picture(image_id):
    image = images.get_picture(image_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/delete_comments", methods=["POST"])
def delete_comments():
    require_login()
    user_id = session["user_id"]
    image_id = request.form["image_id"]
    if not image_id:
        abort(404)
    for comment_id in request.form.getlist("comment_id"):
        images.delete_comment(comment_id, user_id)
    return redirect("/image/" + str(image_id))
