from Phrase_maker import Phrase_Maker
from Name_generator import Name_Generator
import random

class Text_Gen:
    def sentence_generator(self):
        rand_name = Name_Generator()
        p2 = Phrase_Maker("random_adjectives.txt", "random_nouns.txt")
        words_dict = {}
        f = open("random_prepositions.txt")
        words_dict["preposition"] = f.readlines()
        f.close()
        f = open("singular_link_verbs.txt")
        words_dict["singular link verbs"] = f.readlines()
        f.close()
        f = open("plural_link_verbs.txt")
        words_dict["plural link verbs"] = f.readlines()
        f.close()
        f = open("singular_pronouns.txt")
        words_dict["singular pronouns"] = f.readlines()
        f.close()
        f = open("plural_pronouns.txt")
        words_dict["plural pronouns"] = f.readlines()
        f.close()
        phrase2 = p2.generate_random()
        roll = random.random()
        if roll < .5:
            link_verb = random.choice(list(words_dict["singular link verbs"])).strip("\n")
            rand_pronoun = random.choice(list(words_dict["singular pronouns"])).strip("\n")
        else:
            link_verb = random.choice(list(words_dict["plural link verbs"])).strip("\n")
            rand_pronoun = random.choice(list(words_dict["plural pronouns"])).strip("\n")
        vowels = "aeiouAEIOU"

        if roll < .75:
            if phrase2[0] in vowels:
                article_lst = ["an", "the"]
            elif phrase2[0] not in vowels:
                article_lst = ["a", "the"]
            if phrase2[-1] == "s":   # if plural
                article_lst = ["the"]

            new_str = rand_pronoun[0].upper() + rand_pronoun[1:].lower() + " " + link_verb \
                      + " " + random.choice(list(article_lst)).strip("\n") + " " + phrase2 + "."
        else:   # Use random names
            if phrase2[0] in vowels:
                article_lst = ["an", "the"]
            elif phrase2[0] not in vowels:
                article_lst = ["a", "the"]
            if phrase2[-1] == "s":   # if plural
                article_lst = ["the"]
            new_str = rand_name.generate_random() + " " + random.choice(list(words_dict["singular link verbs"])).strip("\n") + " " + random.choice(list(article_lst)).strip(
                "\n") + " " + phrase2 + "."
        return new_str
    def rand_paragraph(self, num_of_sentences=15):
        paragraph = ""
        for i in range(num_of_sentences):
            paragraph += self.sentence_generator() + " "
        return paragraph





