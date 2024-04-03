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


def write_csv(tup, filename: str) -> None:
    """Write tuples to a csv file and save with
    given filename within the /user_uploads folder
    """
    file = filename + ".csv"
    file_path = os.path.join("./user_uploads", file)
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(tup)
    return
