import db

def add_image(title, image_description, genre, user_id, date_added, image):
    sql = """INSERT INTO images (title, image_description, genre, user_id, date_added, image) 
            VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, image_description, genre, user_id, date_added, image])

def get_images():
    sql = "SELECT id, title FROM images ORDER BY id DESC"
    return db.query(sql)

def get_sample_images():
    sql = "SELECT id, title FROM images ORDER BY RANDOM() LIMIT 8"
    return db.query(sql)

def get_image(image_id):
    sql = """SELECT images.id,
                    images.title,
                    images.image_description,
                    images.genre,
                    images.date_added,
                    users.id user_id,
                    users.username
             FROM   images, users
             WHERE  images.user_id = users.id AND
                    images.id = ?"""
    result = db.query(sql, [image_id])
    return result[0] if result else None

def update_image(image_id, title, image_description, genre):
    sql = """UPDATE images SET title = ?,
                               image_description = ?,
                               genre = ?
                           WHERE id = ?"""
    db.execute(sql, [title, image_description, genre, image_id])

def delete_image(image_id):
    sql = "DELETE FROM images WHERE id = ?"
    db.execute(sql, [image_id])

    sql = "DELETE FROM comments WHERE image_id = ?"
    db.execute(sql, [image_id])

    sql = "DELETE FROM grades WHERE image_id = ?"
    db.execute(sql, [image_id])

def find_images(query, genre_query):
    if query and not genre_query:
        sql = """SELECT id, title
                 FROM images
                 WHERE title LIKE ? OR image_description LIKE ?
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
                 WHERE (title LIKE ? OR image_description LIKE ?)
                 AND genre IN ({})
                 ORDER BY id DESC""".format(','.join('?' for _ in genre_query))
        like = "%" + query + "%"
        return db.query(sql, [like, like] + genre_query)
    
    return []

def add_comment(image_id, comment, user_id, date_added, image_title):
    sql = """INSERT INTO comments (image_id, comment, user_id, date_added, image_title) 
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [image_id, comment, user_id, date_added, image_title])

def get_comments(image_id):
    sql = """SELECT comments.id,
                    comments.comment,
                    comments.date_added,
                    comments.user_id,
                    users.username
             FROM   comments
             JOIN   users ON comments.user_id = users.id
             WHERE  comments.image_id = ?
             ORDER BY comments.date_added DESC"""
    result = db.query(sql, [image_id])
    return result if result else None

def delete_comment(comment_id, user_id):
    deletion = "Käyttäjä on poistanut kommentin."
    sql = "UPDATE comments SET comment = ? WHERE id = ? AND user_id = ?"
    db.execute(sql, [deletion, comment_id, user_id])

def add_grade(image_id, user_id, grade):
    grade = int(grade)
    sql = "SELECT image_id, user_id FROM grades WHERE image_id = ? AND user_id = ?"
    result = db.query(sql, [image_id, user_id])
    if result:
        sql = "DELETE FROM grades WHERE image_id = ? AND user_id = ?;"
        db.execute(sql, [image_id, user_id])
    sql = "INSERT INTO grades (image_id, user_id, grade) VALUES (?, ?, ?)"
    db.execute(sql, [image_id, user_id, grade])

def get_grades(image_id):
    sql = """SELECT AVG(grades.grade) AS mean
             FROM   grades
             WHERE  grades.image_id = ?"""
    result = db.query(sql, [image_id])[0]["mean"]
    return round(result, 2) if result else None

def get_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)
    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)
    return classes

def get_picture(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def send_chat(user, chat_message):
    sql = "INSERT INTO chatbox (user, messages) VALUES (?, ?)"
    db.execute(sql, [user, chat_message])

def get_chat():
    sql = "SELECT user, messages FROM chatbox ORDER BY id DESC LIMIT 8"
    return db.query(sql)
