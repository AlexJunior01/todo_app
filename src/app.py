from fastapi import FastAPI

from src.routes.healthcheck import router as health_check_router

app = FastAPI(title='Todo API', version='0.0.1')

app.include_router(health_check_router, prefix='/api', tags=['healthcheck'])
