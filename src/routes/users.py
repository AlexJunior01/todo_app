from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_db, Session
from src.models.user import User
from src.schemas.users import UserInput, UserOutPut
from src.utils.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()


@router.post("/", response_model=UserOutPut)
async def create_user(
        user: UserInput,
        db: Session = Depends(get_db)
):
    user_model = user.dict()
    password = user_model.pop('password')

    user_model = User(**user_model)
    user_model.hashed_password = get_password_hash(password)

    saved, error = user_model.save(db)

    if saved:
        return user_model
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving task",
                     "detail": error}
        )


@router.post('/login')
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    username = form_data.username
    user_model = User().get_by_username(db, username)

    if not user_model:
        return JSONResponse(
            status_code=401,
            content={"message": "Incorrect username or password"}
        )

    if not verify_password(form_data.password, user_model.hashed_password):
        return JSONResponse(
            status_code=401,
            content={"message": "Incorrect username or password"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode = {"sub": username, "user_id": user_model.id}
    access_token = create_access_token(data_to_encode, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
