from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "trustcheck_secret"
ALGORITHM = "HS256"

# Use ARGON2 instead of bcrypt
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

fake_users_db = {}

# -------------------------
# PASSWORD FUNCTIONS
# -------------------------

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

# -------------------------
# USER FUNCTIONS
# -------------------------

def create_user(email: str, password: str):
    if email in fake_users_db:
        return False
    fake_users_db[email] = hash_password(password)
    return True

def authenticate_user(email: str, password: str):
    if email not in fake_users_db:
        return False
    return verify_password(password, fake_users_db[email])

# -------------------------
# TOKEN
# -------------------------

def create_access_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
