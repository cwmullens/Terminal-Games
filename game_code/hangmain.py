import random
import string
import json
from pathlib import Path

# you can edit the list of available terms in "hangman_bank.json"
# not all types of punctuation are accepted right now, but that can be changed by adding them to "taken_letters", found later in the code

settings = {
    "words" : True,
    "phrases" : True,
    "repeats" : True,
    "quotes" : True
}

# prints the available letters
def make_alphabet(letters):
    print(" ".join(letters[:8]))
    print(" ".join(letters[8:17]))
    print(" ".join(letters[17:]))

# prints the blanks representing the hidden phrase
def make_word(word, taken_letters):
    for i in range(len(word)):
        if word[i] not in taken_letters:
            word[i] = "_"
    
    print("".join(word))
    print()

# prints the hanged man
def make_gallows(level):
    # there's a more efficient method to do this but I like seeing the progression in one place
    # the "r" before some of the strings is to stop python from having a conniption over the backslashes
    if level == 0:
        print()
        print()
        print()
        print()
        print()
        print()

    if level == 1:
        print( " _______")
        print(r"      \|")
        print( "       |")
        print( "       |")
        print( "       |")
        print(r"    __/|\__")

    if level == 2:
        print( " _______")
        print(r" |    \|")
        print( "       |")
        print( "       |")
        print( "       |")
        print(r"    __/|\__")

    if level == 3:
        print( " _______")
        print(r" |    \|")
        print( " O     |")
        print( "       |")
        print( "       |")
        print(r"    __/|\__")

    if level == 4:
        print( " _______")
        print(r" |    \|")
        print( " O     |")
        print( " |     |")
        print( "       |")
        print(r"    __/|\__")

    if level == 5:
        print( " _______")
        print(r" |    \|")
        print( " O     |")
        print( "/|     |")
        print( "       |")
        print(r"    __/|\__")

    if level == 6:
        print( " _______")
        print(r" |    \|")
        print( " O     |")
        print(r"/|\    |")
        print( "       |")
        print(r"    __/|\__")

    if level == 7:
        print( " _______")
        print(r" |    \|")
        print( " O     |")
        print(r"/|\    |")
        print( "/      |")
        print(r"    __/|\__")

    if level == 8:
        print( " _______")
        print(r" |    \|")
        print( " O     |")
        print(r"/|\    |")
        print(r"/ \    |")
        print(r"    __/|\__")
    
    print()

# picks a word from hangman_bank, based on difficulty and settings
def choose_word(difficulty, term_hist):
    selection_list = []

    if not settings["words"] and not settings["phrases"]:
        word = random.choice(string.ascii_lowercase)
        return word, None

    filepath = Path(__file__).resolve().parent.parent
    wordbank_path = filepath/"word_banks"/"hangman_bank.json"
    with open(wordbank_path, "r") as f:
        term_banks = json.load(f)
        easy_bank_w = term_banks["easy_word"]
        easy_bank_p = term_banks["easy_phrase"]
        med_bank_w = term_banks["med_word"]
        med_bank_p = term_banks["med_phrase"]
        hard_bank_w = term_banks["hard_word"]
        hard_bank_p = term_banks["hard_phrase"]

    if difficulty == "easy":
        if settings["words"]:
            selection_list.extend(easy_bank_w)
        if settings["phrases"]:
            selection_list.extend(easy_bank_p)
    if difficulty == "medium":
        if settings["words"]:
            selection_list.extend(med_bank_w)
        if settings["phrases"]:
            selection_list.extend(med_bank_p)
    if difficulty == "hard":
        if settings["words"]:
            selection_list.extend(hard_bank_w)
        if settings["phrases"]:
            selection_list.extend(hard_bank_p)

    if len(selection_list) == len(term_hist):
        del term_hist[:]

    # term_hist is used to prevent repeats, can be turned off in settings for a truly random experience
    # you may ask why I don't just use sets in the first place
    # it would be a good question
    mod_selection_list = list(set(selection_list) - set(term_hist))
    if settings["repeats"]:
        word = random.choice(mod_selection_list)
        term_hist.append(word)
    else:
        word = random.choice(selection_list)

    return word, term_hist

def game(difficulty, term_hist):
    over = False

    level = 0
    if difficulty == "medium":
        level = 1
    if difficulty == "hard":
        level = 2

    valid_letters = ["a", "b", "c", "d", "e", "f", "g", "h", 
                     "i", "j", "k", "l", "m", "n", "o", "p", "q", 
                     "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    taken_letters = [" ", ",", ".", "?", "!", "-"]
    wrong_letters = []

    word_str, term_hist = choose_word(difficulty, term_hist)
    word = list(word_str)

    while not over:
        print()
        make_gallows(level)

        make_word(word.copy(), taken_letters)

        make_alphabet(valid_letters)

        # there is an option here because I'm split on which way looks worse while playing
        if settings["quotes"]:
            print(f'Incorrect guesses: {" ".join(f'"{term}"' for term in wrong_letters)}')
        else:
            print(f'Incorrect guesses: {" ".join(wrong_letters)}')

        guess = input("Next guess: ").lower().strip()

        if len(guess) <= 1:
            while guess not in valid_letters or guess == "":
                guess = input("Invalid input, please type a letter from those shown or a phrase: ").lower().strip()
            valid_letters[valid_letters.index(guess)] = " "
        
        # if the guess is incorrect
        if (len(guess) == 1 and guess not in word and guess.upper() not in word) or (len(guess) != 1 and guess != "".join(word).lower()):
                level += 1
                wrong_letters.append(guess)

        taken_letters.append(guess)
        taken_letters.append(guess.upper())

        # if all letters in the term are guessed, or if it is guessed directly
        if set(word).issubset(taken_letters) or guess == "".join(word).lower():
            won = True
            over = True

        if level == 8:
            won = False
            over = True
        
    print()

    if won == True:
        print("You win!")

    if won == False:
        make_gallows(8)
        print("You lose")

    print(f'Phrase: {"".join(word)}')
    print()

    end_command = input('Type "replay" to play the same difficulty, "return" to go back to menu, or "stop" to close: ').lower().strip()
    
    end_commands = ["replay", "return", "stop"]
    while end_command not in end_commands:
        end_command = input('Please type "replay" to play the same difficulty, "return" to go back to menu, or "stop" to close: ').lower().strip()

    if end_command == "replay":
        game(difficulty, term_hist)
    if end_command == "return":
        main()
    if end_command == "stop":
        return
    
def settings_screen():
    global settings
    print()
    print("             Settings")
    print(f"      Allow single words: {settings['words']}")
    print(f"   Allow multi-word phrases: {settings['phrases']}")
    print(f"         No repeats: {settings['repeats']}")
    print(f"Quotes around incorrect guesses: {settings['quotes']}")
    print()
    print('Enter which setting you would like to change, or "return" to go back to title screen: ')
    print('"words", "phrases", "repeats", "quotes"')
    to_edit = input().lower().strip()

    while to_edit != "return" and to_edit not in settings:
        to_edit = input("That is not an accepted input, please type one of the given settings: ").lower().strip()

    if to_edit == "words":
        settings["words"] = not settings["words"]

    if to_edit == "phrases":
        settings["phrases"] = not settings["phrases"]

    if to_edit == "repeats":
            settings["repeats"] = not settings["repeats"]

    if to_edit == "quotes":
        settings["quotes"] = not settings["quotes"]

    if to_edit == "return":
        return
        
    settings_screen()

def title():
    print()
    print("        Terminal Hangman")
    print("           by Chase M")
    print()
    print("              play")
    print("              help")
    print("            settings")
    print()

    command = input('Type "play" to begin, "help" for more info, or "settings" to edit settings: ').lower().strip()

    commands = ["play", "help", "settings"]
    while command not in commands:
        command = input('That is not an accepted input, please type "play", "help", or "settings": ').lower().strip()

    if command == "settings":
        settings_screen()
        difficulty = title()
        return difficulty
    
    if command == "help":
        print()
        print("This is Terminal Hangman, a version of Hangman playable in the terminal.")
        print("Choose letter guesses from the given alphabet, or give the full phrase/word if you know it.")
        print("Watch for punctuation if it is shown, as it must be included in full guesses.")
        print("Some aspects of the gameplay may be changed in the settings.")
        print('The word bank can be edited in "hangman_bank.json".')
        print("Like anything in the terminal, the program can be ended at any point by pressing ctrl+c.")
        input("Once you are done reading this, press enter. ")
        difficulty = title()
        return difficulty

    if command == "play":
        print()
        print("What difficulty level would you like to play?")
        print("easy    medium    hard")
        difficulty = input("Enter which difficulty: ").lower().strip()
        difficulties = ["easy", "medium", "hard"]
        while difficulty not in difficulties:
            difficulty = input('Invalid input, please type "easy", "medium", or "hard": ').lower().strip()

        return difficulty


def main():
    difficulty = title()

    term_hist = []
    game(difficulty, term_hist)

if __name__ == "__main__":
    main()
