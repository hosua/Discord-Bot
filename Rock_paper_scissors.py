import random

class Rock_Paper_Scissors:
    def rockPaperScissors(self, move):
        opponent_roll = random.random()
        result = ""
        if opponent_roll <= 1/3:    # Determine opponent move
            opponent_move = "rock"
        elif opponent_roll <= 2/3:
            opponent_move = "paper"
        else:
            opponent_move = "scissors"

        if move == "rock":  # Determine winner
            if opponent_move == "rock":
                result = "Draw!"
            elif opponent_move == "paper":
                result = "Lose!"
            else:
                result = "Win!"
        if move == "paper":
            if opponent_move == "paper":
                result = "Draw!"
            elif opponent_move == "scissors":
                result = "Lose!"
            else:
                result = "Win!"
        if move == "scissors":
            if opponent_move == "scissors":
                result = "Draw!"
            elif opponent_move == "rock":
                result = "Lose!"
            else:
                result = "Win!"

        return "***" + result + "***" + "\nYour move: " + move + "\nHos Bot's move: " + opponent_move
