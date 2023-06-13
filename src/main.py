from fastapi import FastAPI, Request
from src.routers import route_todo
app = FastAPI()
app.include_router(route_todo.router)
@app.get("/", response_model=SuccessMsg)
def root():
    return {"message": "Welcome to FastAPI"}
