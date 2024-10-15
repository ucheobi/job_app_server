import bcrypt

def get_password_hash(password: str) -> str:
    pwd_bytes  = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt).decode('utf-8')
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_encode = plain_password.encode('utf-8')

    verify = bcrypt.checkpw(password=password_byte_encode, hashed_password=hashed_password.encode('utf-8'))
    return verify