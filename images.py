import db

def add_image(title, kuvaus, genre, user_id, date_added):
    sql = "INSERT INTO images (title, kuvaus, genre, user_id, date_added) VALUES (?, ?, ?, ?, ?)"
    
    db.execute(sql, [title, kuvaus, genre, user_id, date_added])

def get_images():
    sql = "SELECT id, title FROM images ORDER BY id DESC"

    return db.query(sql)

def get_image(image_id):
    sql = """SELECT images.id,
                    images.title,
                    images.kuvaus,
                    images.genre,
                    images.date_added,
                    users.id user_id,
                    users.username
             FROM   images, users
             WHERE  images.user_id = users.id AND
                    images.id = ?"""
    return db.query(sql, [image_id])[0]

def update_image(image_id, title, kuvaus, genre):
    sql = """UPDATE images SET title = ?,
                               kuvaus = ?,
                               genre = ?
                           WHERE id = ?"""
        
    db.execute(sql, [title, kuvaus, genre, image_id])

def delete_image(image_id):
    sql = "DELETE FROM images WHERE id = ?"
        
    db.execute(sql, [image_id])