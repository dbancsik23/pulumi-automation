from fastapi import FastAPI

from app.controllers import create_controller, destroy_controller, list_controller

app = FastAPI()

app.include_router(create_controller.router)
app.include_router(destroy_controller.router)
app.include_router(list_controller.router)