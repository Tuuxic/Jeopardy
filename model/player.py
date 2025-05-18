class Player:
    def __init__(self, id: int, name: str, points: int = 0):
        self.id = id
        self.name = name
        self.points = points


    def __str__(self):
        return f"({self.id}) {self.name}: {self.points} points"
    
    def getDictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "points": self.points
        }