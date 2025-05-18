class State:

    def __init__(self, round: int = 1, categories1: list[str] = [], categories2: list[str] = [], answered: list[int] = []):
        self.round: int = round
        self.categories1: list[str] = categories1
        self.categories2: list[str] = categories2
        self.answered: list[int] = answered

    def get_dictionary(self):
        return {
            "round": self.round,
            "categories1": self.categories1,
            "categories2": self.categories2,
            "answered": self.answered
        }

    def reset(self):
        self.__init__()
    
