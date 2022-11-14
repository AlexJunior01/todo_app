from typing import List, Optional

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models.project import Project
from src.schemas.common import ErrorMessage, Message
from src.schemas.project import ProjectInput, ProjectOutput, ProjectUpdateInput

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


@router.patch('/{project_id}',
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


@router.delete('/{project_id}',
               responses={404: {"model": Message}, 500: {"model": ErrorMessage}},
               response_model=Message
               )
async def delete_projec(
        project_id: int,
        db: Session = Depends(get_db)
):
    project_model = Project.get_by_id(db, project_id)

    if not project_model:
        return JSONResponse(
            status_code=404,
            content={"message": "Project not found."}
        )

    deleted, error = project_model.delete(db)

    if deleted:
        return {"message": "Task deleted"}
    else:
        JSONResponse(
            status_code=500,
            content={"mesage": "Error while deleting project.",
                     "details": error}
        )
