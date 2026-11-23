import os

def print_stage(stage):
    os.system("cls" if os.name == "nt" else "clear")
    print()
    for row in stage:
        for tile in row:
            print(tile, end="")
        print()

def main():
    stage = [
        ["  ,,, "],
        [" (-_-)", "     Snake               Monty Hall"],
        [" | ; |", "    [-----]   Hangman   [----------]"],
        [":::::::", "            [-------]"],
        [":::::::"],
        [":::::::::::::::::::::::::::::::::::::::::::::::::"]
    ]

    print_stage(stage)

    game = input('What do you want to play? Or type "exit" to close the program. ').lower().strip()
    games = ["exit", "snake", "hangman", "monty", "monty hall", "montyhall"]
    while game not in games:
        game = input('Choose from the games listed or type "exit": ').lower().strip()

    if game == "snake":
        # originally coded on Windows, but testing on Mac revealed that other operating systems are picky with giving keyboard access
        print()
        print("Unfortunately, Snake uses the keyboard library, which is not supported on all operating systems.")
        print("In particular, Linux and macOS may require giving additional permissions.")
        play_confirm = input('Would you like to continue? ("y" for continue, anything else to go back) ').lower().strip()
        if play_confirm == "y":
            import game_code.snakemain as snake
            snake.main()

    if game == "hangman":
        import game_code.hangmain as hangman
        hangman.main()

    if game == "monty" or game == "monty hall" or game == "montyhall":
        import game_code.montymain as monty
        monty.main()

    if game == "exit":
        return

    main()

if __name__ == "__main__":
    main()