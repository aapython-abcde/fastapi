import hashlib
from jose import jwt

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"


def hash_password(
   password: str
):
   return hashlib.sha256(
       password.encode("utf-8")
   ).hexdigest()

def verify_password(
   plain_password: str,
   hashed_password: str
):
   return (
       hash_password(plain_password)
       == hashed_password
   )

def create_access_token(user_email: str):
    return jwt.encode(
        {"sub": user_email},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
