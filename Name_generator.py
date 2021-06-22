from Phrase_maker import Phrase_Maker

class Name_Generator:
    def __init__(self):
        self.ng = Phrase_Maker("first_names.txt", "last_names.txt")

    def generate_random(self):
        name = self.ng.generate_random()
        return name
