
class Question:
    def __init__(self, id: int, category: str, value: str, question: str, answer: str, image: str = None, audio: str = None, video: str = None):

        # nid = max([q['id'] for q in qs], default=0) + 1
        self.id = id
        self.category = category
        self.value = value
        self.question = question
        self.answer = answer
        self.image = image 
        self.audio = audio 
        self.video = video 

    def __str__(self):
        return f"Question: {self.question}, Answer: {self.answer}"
    
    def getDictionary(self):
        return {
            "id": self.id,
            "category": self.category,
            "value": self.value,
            "question": self.question,
            "answer": self.answer
        }