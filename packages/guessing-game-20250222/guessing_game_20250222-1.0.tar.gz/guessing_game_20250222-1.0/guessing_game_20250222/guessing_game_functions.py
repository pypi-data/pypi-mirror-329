import random

# Function if the player should guess the number
def human_guessing():
    """
    This is a number guessing game.
    The computer will pick a secret number and the user has to guess it.
    """
    max_number = int(input('The possible number range is 1 to...? '))
    max_attempts = int(input('How many guesses would you like? '))
    secret_number = random.randint(1, max_number)
    guess = None

    for attempt in range(1, max_attempts + 1):
        guess = int(input(f"Guess the number (1-{max_number}): "))
        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print(f"You guessed it! It took {attempt} attempt(s).")
            return

    print('------------------------------------------------------------')
    print(f"Oh no! You ran out of attempts. The number was {secret_number}"
          f"\nYou used all {max_attempts} attempt(s)."
           "\nBetter luck next time!")

# Function if the computer should guess the number
def computer_guessing():
    """
    This is a number guessing game.
    The player will pick a secret number and the computer has to guess it
    """
    max_number = int(input('The possible number range is 1 to...? '))
    max_attempts = int(input('How many guesses do I have? '))
    secret_number = int(input("What is your secret number? I won't tell the computer! "))
    guess = None
    attempt = 0
    lower = 1
    upper = max_number

    for attempt in range(1, max_attempts + 1):
        guess = random.randint(lower, upper)
        if guess < secret_number:
            print(f"The computer guessed {guess}. It's too low. Trying again.")
            lower = guess + 1
        elif guess > secret_number:
            print(f"The computer guessed {guess}. It's too high. Trying again.")
            upper = guess - 1
        else:
            print(f"The computer guessed {guess} correctly! It took {attempt} attempt(s).")
            return

    print('------------------------------------------------------------')
    print("The computer ran out of attempts!" 
          f"\nIt's closest guess was within {abs(secret_number - guess)} numbers"
          f"\nIt used all {max_attempts} attempt(s)."
          "\nBut it will get you next time!")


def guessing_game():
    """
    This is a number guessing game.
    The player can choose to guess the computer's number or 
    for the computer to guess the player's number.
    The game will ask the player to choose who picks the number to guess.
    The game will then start accordingly with the chosen option.
    """

    print("Welcome to the Number Guessing Game!")
    print("You can choose to guess the computer's number")
    print("-- or for the computer to guess your number!")
    print("Who picks the number to guess?")

    choice = str(input("Enter now: Player or Computer " )).strip().lower()

    if choice == "player":
        computer_guessing()
    elif choice == "computer":
        human_guessing()
    else:
        print("Invalid Choice! Please enter 'You' or 'Computer' to start")
