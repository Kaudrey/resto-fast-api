from passlib.context import CryptContext

# Initialize password context (use pbkdf2_sha256)
pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], default="pbkdf2_sha256")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
