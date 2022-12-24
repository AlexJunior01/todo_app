
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models.users import Users
from src.schemas.users import UserInput, UserOutPut
from src.utils.auth import get_password_hash

router = APIRouter()


@router.post("/", response_model=UserOutPut)
async def create_user(
        user: UserInput,
        db: Session = Depends(get_db)
):
    user_model = user.dict()
    password = user_model.pop('password')

    user_model = Users(**user_model)
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
