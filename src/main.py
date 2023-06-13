from fastapi import FastAPI, Request
from src.routers import route_todo, route_auth
from src.schemas import SuccessMsg
app = FastAPI()
app.include_router(route_todo.router)
app.include_router(route_auth.router)
@app.get("/", response_model=SuccessMsg)
def root():
    return {"message": "Welcome to FastAPI"}
