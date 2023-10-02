import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt

def verify_password(password, hashed_password, salt):
    hashed_input_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_input_password == hashed_password