import sys
from . import guessing_game_functions

def main():
    """
    Main function to run the guessing game.

    This function calls three functions from the guessing_game_functions module:
    - guessing_game: Starts the number guessing game, allowing the player to choose who guesses the number.
    - computer_guessing: Initiates a game where the computer attempts to guess the player's secret number.
    - human_guessing: Initiates a game where the player attempts to guess the computer's secret number.
    """

    guessing_game_functions.guessing_game()
    guessing_game_functions.computer_guessing()
    guessing_game_functions.human_guessing()

if __name__ == "__main__":
    main()
