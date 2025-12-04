from pydantic import BaseModel


class DiagramRequest(BaseModel):
    new_diagram: str


class DiagramStorage(BaseModel):
    diagram: str | None = None
    
    def get_diagram(self):
        return self.diagram
    
    def save_diagram(self, new_diagram: str):
        self.diagram = new_diagram

class UserCounter(BaseModel):
    user_count: int = 0

    def increment(self):
        self.user_count += 1
        return self.user_count
    
    def decrement(self):
        if self.user_count > 0:
            self.user_count -= 1
        return self.user_count