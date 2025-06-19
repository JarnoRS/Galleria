import db
from werkzeug.security import check_password_hash, generate_password_hash

def get_user(user_id):
    sql = "SELECT id, username, user_description FROM users WHERE id = ?"  
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_every_user():
    sql = "SELECT id, username FROM users"
    result = db.query(sql)
    return result[0] if result else None

def get_users_images(user_id):
    sql = "SELECT id, title FROM images WHERE user_id = ? ORDER BY id DESC"

    return db.query(sql, [user_id])

def get_user_comments(user_id):
    sql = """SELECT comments.comment,
                    comments.date_added,
                    users.username,
                    comments.image_id,
                    comments.image_title
             FROM   comments
             JOIN   users ON comments.user_id = users.id
             WHERE  comments.user_id = ?
             ORDER BY comments.date_added DESC"""
    result = db.query(sql, [user_id])
    return result if result else None

def create_user(username, password, user_description, profile_pic):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash, user_description, profile_pic) VALUES (?, ?, ?, ?)"
    db.execute(sql, [username, password_hash, user_description, profile_pic])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])[0]
    if not result:
        return None
    user_id = result["id"]
    password_hash = result["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None
    
def update_profile(user_id, image, user_description):
    if image == None:
        sql = "UPDATE users SET user_description = ? WHERE id = ?"
        db.execute(sql, [user_description, user_id])
    else:
        sql = "UPDATE users SET profile_pic = ?, user_description = ? WHERE id = ?"
        db.execute(sql, [image, user_description, user_id])


def get_profile_pic(user_id):
    sql = "SELECT profile_pic FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def delete(user_id):
    sql = "DELETE FROM users WHERE id = ?"
    db.execute(sql, [user_id])

    sql = "DELETE FROM images WHERE user_id = ?"
    db.execute(sql, [user_id])

    sql = "DELETE FROM comments WHERE user_id = ?"
    db.execute(sql, [user_id])

    sql = "DELETE FROM grades WHERE user_id = ?"
    db.execute(sql, [user_id])