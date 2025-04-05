import db
from werkzeug.security import check_password_hash, generate_password_hash

def get_user(user_id):
    sql = "SELECT id, username, kuvaus FROM users WHERE id = ?"
    
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_users_images(user_id):
    sql = "SELECT id, title FROM images WHERE user_id = ? ORDER BY id DESC"

    return db.query(sql, [user_id])

def create_user(username, password, kuvaus):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash, kuvaus) VALUES (?, ?, ?)"
    db.execute(sql, [username, password_hash, kuvaus])

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