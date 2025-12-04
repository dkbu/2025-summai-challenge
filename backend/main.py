from typing import Annotated
from fastapi import FastAPI, Depends
from models import DiagramStorage, DiagramRequest, UserCounter


app = FastAPI()


# Create a global instance or use a proper dependency pattern
diagram_storage = DiagramStorage()
user_counter = UserCounter()


async def get_diagram_storage():
    return diagram_storage


async def get_user_counter():
    return user_counter


@app.get("/diagram")
async def get_diagram(d: Annotated[DiagramStorage, Depends(get_diagram_storage)]):
    return {"diagram": d.get_diagram()}


@app.post("/diagram")
async def save_diagram(request: DiagramRequest, d: Annotated[DiagramStorage, Depends(get_diagram_storage)]):
    d.save_diagram(request.new_diagram)
    return {"status": "Diagram saved"}


@app.post("/user")
async def add_user(users: Annotated[UserCounter, Depends(get_user_counter)]):
    users.increment()
    return {"status": "User added"}


@app.delete("/user")
async def delete_user(users: Annotated[UserCounter, Depends(get_user_counter)]):
    users.decrement()
    return {"status": "User deleted"}


@app.get("/users")
async def get_users(users: Annotated[UserCounter, Depends(get_user_counter)]):
    return {"user_count": users.user_count}