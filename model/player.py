from pydantic import BaseModel

class Player(BaseModel):
    id: int 
    name: str 
    points: int

    def __init__(self, id: int, name: str, points: int = 0):
        super().__init__(id=id, name=name, points=points)


    def __str__(self):
        return f"({self.id}) {self.name}: {self.points} points"
    
    def to_json(self):
        return self.model_dump()
    