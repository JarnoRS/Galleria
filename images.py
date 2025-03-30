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

def find_images(query, genre_query):
    if query and not genre_query:
        sql = """SELECT id, title
                 FROM images
                 WHERE title LIKE ? OR kuvaus LIKE ?
                 ORDER BY id DESC"""
        like = "%" + query + "%"
        return db.query(sql, [like, like])

    elif genre_query and not query:
        sql = """SELECT id, title
                 FROM images
                 WHERE genre IN ({})
                 ORDER BY id DESC""".format(','.join('?' for _ in genre_query))
        
        return db.query(sql, genre_query)

    elif query and genre_query:
        sql = """SELECT id, title
                 FROM images
                 WHERE (title LIKE ? OR kuvaus LIKE ?)
                 AND genre IN ({})
                 ORDER BY id DESC""".format(','.join('?' for _ in genre_query))
        
        like = "%" + query + "%"
        return db.query(sql, [like, like] + genre_query)
    
    return []