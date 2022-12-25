from datetime import timedelta, datetime

from jose import jwt

from src.auth import pwd_context
from src.config import SECRET_KEY, ALGORITHM


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hased_password: str) -> bool:
    return pwd_context.verify(plain_password, hased_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    data_to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)

    data_to_encode.update({'expire': str(expire)})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
