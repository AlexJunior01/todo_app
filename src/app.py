from fastapi import FastAPI

from src.routes.healthcheck import router as health_check_router
from src.routes.task import router as task_router
from src.utils.database import run_migration

app = FastAPI(title='Todo API', version='0.0.2')

app.include_router(health_check_router, prefix='/api', tags=['healthcheck'])
app.include_router(task_router, prefix='/task', tags=['task'])


@app.on_event('startup')
async def start_app():
    try:
        run_migration('upgrade', 'head')
    except Exception as err:  # pylint: disable=W0703
        print("ERROR:", err)
