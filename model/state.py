from pydantic import BaseModel 

class State(BaseModel):
    round: int 
    categories1: list[str]
    categories2: list[str]
    answered: list[int]

    def __init__(self, round: int = 1, categories1: list[str] = [], categories2: list[str] = [], answered: list[int] = []):
        super().__init__(round=round, categories1=categories1, categories2=categories2, answered=answered)


    def reset(self):
        self.__init__()


    def to_json(self):
        return self.model_dump()
    
