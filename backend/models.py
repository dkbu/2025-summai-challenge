from pydantic import BaseModel, Field, field_validator


class DiagramRequest(BaseModel):
    new_diagram: str = Field(..., min_length=1, max_length=10*1024*1024, description="BPMN diagram XML content")
    
    @field_validator('new_diagram')
    def validate_diagram_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Diagram content cannot be empty')
        
        # Basic check for XML-like content
        v_stripped = v.strip()
        if not (v_stripped.startswith('<') and v_stripped.endswith('>')):
            raise ValueError('Diagram content must be valid XML')
            
        return v


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