from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash_(password):    
    hashedPassword = pwd_cxt.hash(password)
    return hashedPassword

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_cxt.verify(plain_password, hashed_password)