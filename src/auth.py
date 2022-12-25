from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.config import SECRET_KEY, ALGORITHM
from src.database import get_db, Session
from src.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")

    try:
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = User().get_by_id(db, user_id)

    return user
