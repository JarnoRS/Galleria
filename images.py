import db

def add_image(title, kuvaus, genre, user_id, date_added):
    sql = "INSERT INTO images (title, kuvaus, genre, user_id, date_added) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, kuvaus, genre, user_id, date_added])

def get_images():
    sql = "SELECT id, title FROM images ORDER BY id DESC"

    return db.query(sql)

def get_image(image_id):
    sql = """SELECT images.title,
                    images.kuvaus,
                    images.genre,
                    images.date_added,
                    users.username
             FROM   images, users
             WHERE  images.user_id = users.id AND
                    images.id = ?"""
    return db.query(sql, [image_id])[0]