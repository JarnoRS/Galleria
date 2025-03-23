import db

def add_item(title, kuvaus, genre, user_id):
    sql = "INSERT INTO images (title, kuvaus, genre, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, kuvaus, genre, user_id])