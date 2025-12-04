from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

class DiagramStorage:
    def __init__(self):
        self.diagram = None
    
    def get_diagram(self):
        return self.diagram
    
    def save_diagram(self, new_diagram: str):
        self.diagram = new_diagram


async def diagram(d: DiagramStorage):
    return d


@app.get("/get-diagram")
async def get_diagram(d: Annotated[DiagramStorage, Depends(diagram)]):
    return {"diagram": d.get_diagram()}

@app.post("/save-diagram")
async def save_diagram(new_diagram: str, d: Annotated[DiagramStorage, Depends(diagram)]):
    d.save_diagram(new_diagram)
    return {"status": "Diagram saved"}