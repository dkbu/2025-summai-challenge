from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import DiagramStorage, DiagramRequest, UserCounter
from dependencies import get_diagram_storage, get_user_counter
import xml.etree.ElementTree as ET


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
    # Validate the diagram content
    if not request.new_diagram or not request.new_diagram.strip():
        raise HTTPException(status_code=400, detail="Diagram content cannot be empty")
    
    # Check diagram size (prevent extremely large payloads)
    if len(request.new_diagram) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=413, detail="Diagram content too large (max 10MB)")
    
    # Validate XML structure
    try:
        ET.fromstring(request.new_diagram)
    except ET.ParseError as e:
        raise HTTPException(status_code=400, detail=f"Invalid XML format: {str(e)}")
    
    # Check if it's a BPMN diagram (basic validation)
    if "bpmn" not in request.new_diagram.lower() and "definitions" not in request.new_diagram:
        raise HTTPException(status_code=400, detail="Content does not appear to be a valid BPMN diagram")
    
    d.save_diagram(request.new_diagram)
    return {"status": "Diagram saved", "size": len(request.new_diagram)}


@app.post("/user")
async def add_user(users: Annotated[UserCounter, Depends(get_user_counter)]):
    # Prevent user count from going too high (basic DoS protection)
    if users.user_count >= 1000:
        raise HTTPException(status_code=429, detail="Maximum user limit reached")
    
    current_count = users.increment()
    return {"status": "User added", "user_count": current_count}


@app.delete("/user")
async def delete_user(users: Annotated[UserCounter, Depends(get_user_counter)]):
    if users.user_count <= 0:
        raise HTTPException(status_code=400, detail="No users to remove")
    
    current_count = users.decrement()
    return {"status": "User deleted", "user_count": current_count}


@app.get("/users")
async def get_users(users: Annotated[UserCounter, Depends(get_user_counter)]):
    return {"user_count": users.user_count}


@app.post("/cleanup")
async def cleanup_user(users: Annotated[UserCounter, Depends(get_user_counter)]):
    """Handle cleanup requests from sendBeacon during page unload"""
    if users.user_count <= 0:
        return {"status": "No users to cleanup", "user_count": 0}
    
    current_count = users.decrement()
    return {"status": "User cleanup completed", "user_count": current_count}