from typing import List, Optional

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models.project import Project
from src.models.task import Task
from src.schemas.common import ErrorMessage, Message
from src.schemas.project import ProjectInput, ProjectOutput, ProjectUpdateInput
from src.schemas.task import TaskOutput

router = APIRouter()


@router.get('/', response_model=List[ProjectOutput])
async def get_all_projects(db: Session = Depends(get_db)):
    return Project.get_all(db)


@router.get('/{project_id}', responses={404: {"model": Message}}, response_model=ProjectOutput)
async def get_project(
        project_id: int,
        db: Session = Depends(get_db)
):
    project = Project().get_by_id(db, project_id)

    if not project:
        return JSONResponse(
            status_code=404,
            content={"message": "Project not found."}
        )

    return project


@router.post('/', responses={500: {"model": ErrorMessage}}, response_model=ProjectOutput)
async def create_project(
        project_input: ProjectInput,
        db: Session = Depends(get_db)
):
    project_model = Project(**project_input.dict())
    saved, error = project_model.save(db)

    if saved:
        return project_model
    else:
        JSONResponse(
            status_code=500,
            content={"mesage": "Error while saving project.",
                     "details": error}
        )


@router.patch(
    '/{project_id}',
    responses={404: {"model": Message}, 500: {"model": ErrorMessage}},
    response_model=Message)
async def update_project(
        project_id: int,
        project_payload: ProjectUpdateInput,
        db: Session = Depends(get_db)
):
    project_model = Project.get_by_id(db, project_id)

    if not project_model:
        return JSONResponse(
            status_code=404,
            content={"message": "Project not found."}
        )

    updated, error = project_model.update(db, project_payload.dict(exclude_none=True))

    if updated:
        return {"message": "Task updated"}
    else:
        JSONResponse(
            status_code=500,
            content={"mesage": "Error while updating project.",
                     "details": error}
        )


@router.delete(
    '/{project_id}',
    responses={404: {"model": ErrorMessage}, 500: {"model": ErrorMessage}},
    response_model=Message
)
async def delete_project(
        project_id: int,
        delete_tasks: Optional[bool] = False,
        db: Session = Depends(get_db)
):
    project_model = Project.get_by_id(db, project_id)

    if not project_model:
        return JSONResponse(
            status_code=404,
            content={"message": "Project not found."}
        )

    if delete_tasks:
        for task in project_model.tasks:
            task.delete(db)

    deleted, error = project_model.delete(db)

    if deleted:
        return {"message": "Project deleted"}
    else:
        JSONResponse(
            status_code=500,
            content={"mesage": "Error while deleting project.",
                     "details": error}
        )


@router.post(
    '/{project_id}/task',
    responses={400: {"model": ErrorMessage}, 404: {"model": ErrorMessage}, 500: {"model": ErrorMessage}},
    response_model=Message
)
async def add_task_to_project(
        project_id: int,
        task_ids: List[int],
        db: Session = Depends(get_db)
):
    project_model = Project.get_by_id(db, project_id)

    if not project_model:
        return JSONResponse(
            status_code=404,
            content={"message": "Project not found."}
        )

    non_existen_ids = Task.get_non_existent_ids(db, task_ids)

    if non_existen_ids:
        return JSONResponse(
            status_code=400,
            content={"message": f"Task_ids {non_existen_ids} do not exist."}
        )

    tasks = Task.get_by_ids(db, task_ids)

    added, error = project_model.add_tasks(db, tasks)

    if added:
        return {"message": "Tasks added to the project"}
    else:
        JSONResponse(
            status_code=500,
            content={"mesage": "Error while adding tasks to project.",
                     "details": error}
        )


@router.delete(
    '/{project_id}/task',
    responses={400: {"model": ErrorMessage}, 404: {"model": ErrorMessage}, 500: {"model": ErrorMessage}},
    response_model=Message
)
async def delete_tasks_from_project(
        project_id: int,
        task_ids: List[int],
        db: Session = Depends(get_db)
):
    project_model = Project.get_by_id(db, project_id)

    if not project_model:
        return JSONResponse(
            status_code=404,
            content={"message": "Project not found."}
        )

    non_existen_ids = Task.get_non_existent_ids(db, task_ids)

    if non_existen_ids:
        return JSONResponse(
            status_code=400,
            content={"message": f"Task_ids {non_existen_ids} do not exist."}
        )

    tasks = Task.get_by_ids(db, task_ids)

    removed, error = project_model.remove_tasks(db, tasks)

    if removed:
        return {"message": "Tasks removed from the project"}
    else:
        JSONResponse(
            status_code=500,
            content={"mesage": "Error while removing tasks to project.",
                     "details": error}
        )


@router.get(
    '/{project_id}/task',
    responses={404: {"model": ErrorMessage}},
    response_model=List[TaskOutput]
)
async def get_all_tasks_linked_to_project(
        project_id: int,
        db: Session = Depends(get_db)
):
    project_model = Project.get_by_id(db, project_id)

    if not project_model:
        return JSONResponse(
            status_code=404,
            content={"message": "Project not found."}
        )

    return project_model.tasks
