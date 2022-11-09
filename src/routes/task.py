from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models.task import Task
from src.schemas.common import ErrorMessage, Message
from src.schemas.task import TaskInput, TaskOutput, TaskUpdateInput


router = APIRouter()


@router.get('/', response_model=List[TaskOutput])
async def get_all_tasks(db: Session = Depends(get_db)):
    return Task.get_all(db)


@router.get('/{task_id}', responses={404: {"model": ErrorMessage}}, response_model=TaskOutput)
async def get_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = Task.get_by_id(db, task_id)
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
    saved, error = task_model.save(db)

    if saved:
        return task_model
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving task",
                     "detail": error}
        )


@router.patch('/{task_id}', responses={404: {"model": ErrorMessage}}, response_model=Message)
async def update_task(
        task_id: int,
        task_payload: TaskUpdateInput,
        db: Session = Depends(get_db)
):
    task = Task.get_by_id(db, task_id)

    if not task:
        return JSONResponse(
            status_code=404,
            content={"message": "Task not found"}
        )

    updated, error = task.update(db, task_payload.dict(exclude_none=True))

    if updated:
        return {"message": "Task updated"}
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating task",
                     "detail": error}
        )


@router.delete('/{task_id}', responses={404: {"model": ErrorMessage}}, response_model=Message)
async def delete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = Task.get_by_id(db, task_id)

    if not task:
        return JSONResponse(
            status_code=404,
            content={"message": "Task not found"}
        )

    deleted, error = task.delete(db)

    if deleted:
        return {"message": "Task deleted"}
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating task",
                     "detail": error}
        )
