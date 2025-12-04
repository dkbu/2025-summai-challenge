from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import DiagramStorage, DiagramRequest, UserCounter
from dependencies import get_diagram_storage, get_user_counter


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


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


@app.post("/cleanup")
async def cleanup_user(users: Annotated[UserCounter, Depends(get_user_counter)]):
    """Handle cleanup requests from sendBeacon during page unload"""
    users.decrement()
    return {"status": "User cleanup completed"}