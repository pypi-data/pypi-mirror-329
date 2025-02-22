import random

class VegasAI:
    def __init__(self):
        pass
    def pick_winner(self, participants:list):
        if not participants:
            raise ValueError("participants list cannt be empty")
        return random.choice(participants)
    def pick_looser(self, participants:list):
        if not participants:
            raise ValueError("participants list cannt be empty")
        return random.choice(participants)