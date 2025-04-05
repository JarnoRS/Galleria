import db

def get_user(user_id):
    sql = "SELECT id, username, kuvaus FROM users WHERE id = ?"
    
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_users_images(user_id):
    sql = "SELECT id, title FROM images WHERE user_id = ? ORDER BY id DESC"

    return db.query(sql, [user_id])