from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models.task import Task
from src.schemas.common import ErrorMessage, Message
from src.schemas.task import TaskInput, TaskOutput, TaskUpdateInput
from src.utils.database import update_object


router = APIRouter()


@router.get('/', response_model=List[TaskOutput])
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@router.get('/{task_id}', responses={404: {"model": ErrorMessage}}, response_model=TaskOutput)
async def get_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter_by(id=task_id).first()
    if task:
        return task
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Task not found"}
        )


@router.post('/', response_model=TaskOutput)
async def create_task(
        task: TaskInput,
        db: Session = Depends(get_db)
):
    task_model = Task(**task.dict())
    try:
        db.add(task_model)
        db.commit()
        if task_model.title:
            return task_model
    except SQLAlchemyError as error:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving task",
                     "detail": error.args}
        )


@router.patch('/{task_id}')
async def update_task(
        task_id: int,
        task_payload: TaskUpdateInput,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter_by(id=task_id).first()

    if not task:
        return JSONResponse(
            status_code=404,
            content={"message": "Task not found"}
        )

    update_object(db, task, task_payload.dict(exclude_none=True))
    return {"message": "Task updated"}


@router.delete('/{task_id}', responses={404: {"model": ErrorMessage}}, response_model=Message)
async def delete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter_by(id=task_id).first()

    if not task:
        return JSONResponse(
            status_code=404,
            content={"message": "Task not found"}
        )

    db.delete(task)
    db.commit()

    return JSONResponse(
            status_code=200,
            content={"message": "Task deleted"}
    )
