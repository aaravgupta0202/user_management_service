# auth_handler.py

from datetime import datetime, timedelta
import traceback
import time
import jwt


SECRET_KEY = "HSDFSFKR123473"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int, email: str):
    payload = {
        "user_id": user_id,
        "email": email,
        "expires": time.time() + 86400
        # "expires": time.time() + 12000
            }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    tokenResponse = {
        "access_token": token
    }
    return tokenResponse

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
