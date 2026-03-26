import random

COLORS = ["Red", "Blue", "Green", "Yellow"]
NUMBERS = list(range(10))
SKIP = "Skip"

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def is_skip(self):
        return self.value == SKIP

    def __repr__(self):
        return f"{self.color} {self.value}"
