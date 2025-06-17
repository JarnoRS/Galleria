import db
from werkzeug.security import check_password_hash, generate_password_hash

def get_user(user_id):
    sql = "SELECT id, username, kuvaus FROM users WHERE id = ?"
    
    result = db.query(sql, [user_id])
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

def create_user(username, password, kuvaus, profile_pic):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash, kuvaus, profile_pic) VALUES (?, ?, ?, ?)"
    db.execute(sql, [username, password_hash, kuvaus, profile_pic])

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
    
def update_profile(user_id, image, kuvaus):
    if image == None:
        sql = "UPDATE users SET kuvaus = ? WHERE id = ?"
        db.execute(sql, [kuvaus, user_id])
    else:
        sql = "UPDATE users SET profile_pic = ?, kuvaus = ? WHERE id = ?"
        db.execute(sql, [image, kuvaus, user_id])


def get_profile_pic(user_id):
    sql = "SELECT profile_pic FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None