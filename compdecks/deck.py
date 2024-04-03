from csv import reader
from random import shuffle


class Deck:
    def __init__(self, path: str):
        self.questions: list[tuple] = []
        self.load(path)

    def load(self, path: str) -> None:
        with open(path, "r", newline="") as file:
            rder = reader(file)
            for row in rder:
                if len(row) == 2:
                    question, answer = row
                    self.questions.append((question, answer))
            shuffle(self.questions)
