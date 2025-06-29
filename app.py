import secrets
import sqlite3
from datetime import datetime, date

from flask import Flask
from flask import abort, redirect, render_template, request, session, make_response, flash
import markupsafe

import config
import db
import images
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        flash("VIRHE: Väärä tunnus tai salasana")
        return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
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
            flash("VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto")
            return redirect("/register")
        profile_pic = file.read()
        if len(profile_pic) > 100 * 1024:
            flash("VIRHE: Lähettämäsi tiedosto on liian suuri (Yli 100 kt)")
            return redirect("/register")
    if len(password1) < 5:
        flash("VIRHE: Antamasi salasana on liian lyhyt (Alle 5 merkkiä)")
        return redirect("/register")
    if password1 != password2:
        flash("VIRHE: Antamasi salasanat eivät täsmää")
        return redirect("/register")
    try:
        users.create_user(username, password1, user_description, profile_pic)
    except sqlite3.IntegrityError:
        flash("VIRHE: Tunnus on jo käytössä")
        return redirect("/register")
    return render_template("user_created.html", username=username)

@app.route("/edit_user/<int:user_id>")
def edit_user(user_id):
    require_login()
    user_id = session["user_id"]
    user = users.get_user(user_id)
    chat = images.get_chat()
    return render_template("edit_user.html", user=user, chat=chat)

@app.route("/update_user", methods=["POST"])
def update_user():
    require_login()
    check_csrf()
    user_id = request.form["user_id"]
    file = request.files["image"]
    user_description = request.form["description"]
    if file:
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto")
            return redirect("/edit_user")
        image = file.read()
        if len(image) > 100 * 1024:
            flash("VIRHE: Lähettämäsi tiedosto on liian suuri (Yli 100 kt)")
            return redirect("/edit_user")
        user_id = session["user_id"]
        if user_id != session["user_id"]:
            abort(403)
        users.update_profile(user_id, image, user_description)
        return redirect("/user/" + str(user_id))
    users.update_profile(user_id, None, user_description)
    return redirect("/user/" + str(user_id))

@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
    require_login()
    user_id = session["user_id"]
    user = users.get_user(user_id)
    if request.method == "GET":
        chat = images.get_chat()
        return render_template("delete_user.html", user=user, chat=chat)
    if request.method == "POST":
        check_csrf()
        password = request.form["password"] 
        if not users.verify_password(user["username"], password):
            flash("VIRHE: Väärä salasana")
            return redirect("delete_user")
        try:
            users.delete(user_id)
            session.clear()
            return redirect("/")
        except Exception as e:
            return redirect("/user/" + str(user_id)) 

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    users_images = users.get_users_images(user_id)
    comments = users.get_user_comments(user_id) or []
    comments = comments[:3]
    chat = images.get_chat()
    return render_template("show_user.html", user=user, users_images=users_images, comments=comments, chat=chat)

@app.route("/all_users")
def all_users():
    every_user = users.get_every_user()
    chat = images.get_chat()
    return render_template("all_users.html", every_user=every_user, chat=chat)

@app.route("/add_image")
def add_image():
    require_login()
    classes = images.get_classes()
    chat = images.get_chat()
    return render_template("add_image.html", classes=classes, chat=chat)

@app.route("/create_image", methods=["POST"])
def create_image():
    require_login()
    check_csrf()
    title = request.form["title"]
    if not title or len(title) > 50:
        flash("VIRHE: Tyhjä otsikko tai otsikon pituus yli 50 merkkiä")
        return redirect("/add_image")
    image_description = request.form["description"]
    if len(image_description) > 1000:
        flash("VIRHE: Kuvauksen pituus yli 1000 merkkiä")
        return redirect("/add_image")
    genre = request.form["genre"]
    classes = images.get_classes()
    if genre not in classes["genre"]:
        abort(403)
    file = request.files["profile_pic"]
    if not file.filename.endswith(".jpg"):
        flash("VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto")
        return redirect("/add_image")
    image = file.read()
    if len(image) > 1000 * 1024:
        flash("VIRHE: Lähettämäsi tiedosto on liian suuri (Yli 1 mt)")
        return redirect("/add_image")
    user_id = session["user_id"]
    date_added = date.today()
    images.add_image(title, image_description, genre, user_id, date_added, image)
    return redirect("/")

@app.route("/edit_image/<int:image_id>")
def edit_image(image_id):
    require_login()
    classes = images.get_classes()
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if image["user_id"] != session["user_id"]:
        abort(403)
    chat = images.get_chat()
    return render_template("edit_image.html", image=image, classes=classes, chat=chat)

@app.route("/update_image", methods=["POST"])
def update_image():
    require_login()
    check_csrf()
    image_id = request.form["image_id"]
    title = request.form["title"]
    if not title or len(title) > 50:
        flash("VIRHE: Tyhjä otsikko tai otsikon pituus yli 50 merkkiä")
        return redirect("/edit_image")
    image_description = request.form["description"]
    if len(image_description) > 1000:
        flash("VIRHE: Kuvauksen pituus yli 1000 merkkiä")
        return redirect("/edit_image")
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
    chat = images.get_chat()
    return redirect("/image/" + str(image_id), chat=chat)

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
    chat = images.get_chat()
    return render_template("find_image.html", query=query, genre_query=genre_query,results=results, chat=chat)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = images.get_image(image_id)
    comments = images.get_comments(image_id)
    grade_mean = images.get_grades(image_id)
    if not image:
        abort(404)
    chat = images.get_chat()
    return render_template("show_image.html", image=image, comments=comments, grade_mean=grade_mean, chat=chat)

@app.route("/delete_image/<int:image_id>", methods=["GET", "POST"])
def delete_image(image_id):
    require_login()
    check_csrf()
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if image["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        chat = images.get_chat()
        return render_template("delete_image.html", image=image, chat=chat)
    if request.method == "POST":
        if "remove" in request.form:
            images.delete_image(image_id)
            return redirect("/")
        return redirect("/image/" + str(image_id))

@app.route("/send_chat", methods=["POST"])
def send_chat():
    require_login()
    check_csrf()
    chat_message = request.form["chat_message"]
    images.send_chat(session["username"], chat_message)
    return redirect(request.referrer or '/')

@app.route("/")
def index():
    sample_images = images.get_sample_images()
    chat = images.get_chat()
    return render_template("index.html", images=sample_images, chat=chat)

@app.route("/add_comment/<int:image_id>", methods=["POST"])
def add_comment(image_id):
    require_login()
    check_csrf()
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
    return redirect("/image/" + str(image_id))

@app.route("/delete_comments", methods=["POST"])
def delete_comments():
    require_login()
    check_csrf()
    user_id = session["user_id"]
    image_id = request.form["image_id"]
    if not image_id:
        abort(404)
    for comment_id in request.form.getlist("comment_id"):
        images.delete_comment(comment_id, user_id)
    return redirect("/image/" + str(image_id))

@app.route("/add_grade/<int:image_id>", methods=["POST"])
def add_grade(image_id):
    require_login()
    check_csrf()
    image = images.get_image(image_id)
    if not image:
        abort(404)
    if "user_id" in session:
        image_id = image["id"]
        grade = request.form["grade"]
        user_id = session["user_id"]
        if grade:
            images.add_grade(image_id, user_id, grade)
    return redirect("/image/" + str(image_id))

@app.route("/picture/<int:image_id>")
def show_picture(image_id):
    image = images.get_picture(image_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/profile_pic/<int:user_id>")
def show_profile_pic(user_id):
    image = users.get_profile_pic(user_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response
