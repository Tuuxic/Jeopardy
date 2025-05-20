from pydantic import BaseModel
from typing import Optional


class Question(BaseModel):
    id: int
    category: str
    value: int 
    question: str
    answer: str
    image: Optional[str] 
    audio: Optional[str] 
    video: Optional[str] 

    def __init__(self, id: int, category: str, value: str, question: str, answer: str, image: str = None, audio: str = None, video: str = None):
        super().__init__(id=id, category=category, value=value, question=question, answer=answer, image=image, audio=audio, video=video)    

    def __str__(self):
        return f"Question: {self.question}, Answer: {self.answer}"

    def to_json(self):
        return self.model_dump()
    