import uuid
from datetime import datetime, timedelta
from jose import jwt, JWTError
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRY_HOURS


def create_guest_token():
    guest_id = str(uuid.uuid4())
    payload = {
        "sub": guest_id,
        "type": "guest",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token, guest_id


def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        guest_id = payload.get("sub")
        if not guest_id:
            return None
        return guest_id
    except JWTError:
        return None