import random
# For two words
class Phrase_Maker:
    def __init__(self, first_name_file, last_name_file):
        self.first_word_file = first_name_file
        self.last_word_file = last_name_file

    def dict_maker(self, first_file, last_file):
        d = {"First": [], "Last": []}
        f = open(first_file, "r")
        line_lst = f.readlines()
        f.close()
        for name in line_lst:
            d["First"].append(name.strip("\n"))  # Get rid of "\n"

        f = open(last_file, "r")
        line_lst = f.readlines()
        f.close()
        for name in line_lst:
            d["Last"].append(name.strip("\n"))
        return d

    def generate_random(self):
        name_dict = self.dict_maker(self.first_word_file, self.last_word_file)
        name_dict = name_dict
        first = name_dict["First"][random.randint(0, len(name_dict["First"])-1)]
        last = name_dict["Last"][random.randint(0, len(name_dict["Last"])-1)]
        return first + " " + last

