import random
import time

def print_board(board):
    print()
    for row in board:
        for tile in row:
            print(tile, end = "")
        print("")

def make_board():
    # there are a lot of possible permutations so after this initialization the board is edited by coordinates
    board_strings = [
        "                                       ",
        "  ,,,      ,_____,   ,_____,   ,_____, ",
        " (-_-)     |     |   |     |   |     | ",
        " | ; |     |  1  |   |  2  |   |  3  | ",
        ":::::::    |    .|   |    .|   |    .| ",
        ":::::::    |_____|   |_____|   |_____| ",
        ":::::::::::::::::::::::::::::::::::::::"
    ]

    board = []
    for string in board_strings:
        board.append(list(string))

    return board

def create_puzzle():
    puzzle_dic = {1: "nothing", 2: "nothing", 3: "nothing"}

    prize_door = random.randint(1, 3)
    puzzle_dic[prize_door] = "prize"

    return puzzle_dic

def help_screen(board):
    print()
    print("This is a playable version of the Monty Hall problem.")
    print("Here, there is a cash prize in one door and nothing behind the other two.")
    print("After selecting the initial door, an empty one is shown,")
    print("and there is the opportunity to switch to the remaining door.")
    print("This problem is infamous for its unintuitive conclusion:")
    print("switching is the correct decision 66.6 percent of the time.")
    print("There are a few ways to conceptualize why this is true,")
    print("and this game is a very slow way.")
    print("Like anything in the terminal, the program can be ended at any point by pressing ctrl+c.")
    input("To return to the game, press enter: ")
    chosen_door, ret_board = choose(board)
    return chosen_door, ret_board

def choose(board):
    print_board(board)
    choices = ["1", "2", "3", "help"]
    chosen_door = input('Choose a door, or type "help": ').lower().strip()
    while chosen_door not in choices:
        chosen_door = input('Please choose door "1", "2", or "3" or type "help" for information: ').lower().strip()

    if chosen_door == "help":
        chosen_door, board = help_screen(board)
        return chosen_door, board

    int_chosen_door = int(chosen_door)

    # creates an arrow pointing at the chosen door
    board[0][14 + (10 * (int_chosen_door - 1))] = "v"

    print_board(board)
    time.sleep(2)

    return int_chosen_door, board

def show(puzzle_dic, chosen_door, board):
    # randomly selects an empty, unselected door to reveal
    potential_shows = []
    for door in puzzle_dic:
        if not door == chosen_door and puzzle_dic[door] == "nothing":
            potential_shows.append(door)
    shown_door = random.choice(potential_shows)

    # visually opens an empty door
    offset = 10 * (shown_door - 1)
    for i in range(4):
        board[3 + i][9 + offset] = "|"
    for i in range(2):
        board[2 + (4 * i)][10 + offset] = "/"
    board[5][10 + offset] = "."
    board[3][14 + offset] = " "
    board[4][16 + offset] = " "

    print_board(board)

    return shown_door, board

def switch_door(puzzle_dic, chosen_door, shown_door, board):
    switch = input('Would you like to switch doors? ("y" for yes, anything else for no): ').lower().strip()

    if switch == "y":
        # removes previous arrow
        board[0][14 + (10 * (chosen_door - 1))] = " "

        for door in puzzle_dic:
            if door != chosen_door and door != shown_door:
                # had to change the variable name due to strange behavior, likely from collision with the parameter
                chosen_door_var = door

                # new arrow
                board[0][14 + (10 * (chosen_door_var - 1))] = "v"
    else:
        chosen_door_var = chosen_door

    print_board(board)
    time.sleep(2)
            
    return chosen_door_var, board

def reveal(puzzle_dic, chosen_door, board):
    # visually opens the last two doors
    for i in range(3):
        offset = 10 * i
        for j in range(4):
            board[3 + j][9 + offset] = "|"
        for j in range(2):
            board[2 + (4 * j)][10 + offset] = "/"
        board[5][10 + offset] = "."
        board[3][14 + offset] = " "
        board[4][16 + offset] = " "

    for door in puzzle_dic:
        if puzzle_dic[door] == "prize":
            prize_door = door
            break
    
    # puts dollar signs behind the prize door
    # there is a more compact way to write this with one big loop but it looks ugly
    offset = 10 * (prize_door - 1)
    for i in range(2):
        board[3][14 + i + offset] = "$"
    for i in range(3):
        board[4][13 + i + offset] = "$"
    for i in range(5):
        board[5][12 + i + offset] = "$"


    if puzzle_dic[chosen_door] == "prize":
        print_board(board)
        print("win")
        return True
    else:
        # gives the host beady eyes
        for i in range(2):
            board[2][2 + (i * 2)] = "."
        print_board(board)
        print("lose")
        return False
    
def game(wins, losses):
    board = make_board()
    puzzle = create_puzzle()
    chosen_door, board = choose(board)

    shown_door, board = show(puzzle, chosen_door, board)
    chosen_door, board = switch_door(puzzle, chosen_door, shown_door, board)
    correct = reveal(puzzle, chosen_door, board)

    if correct:
        wins += 1
    else:
        losses += 1
    
    print(f"Total games: {wins + losses}, total wins: {wins}, total losses: {losses}")

    end_command = input('Replay? ("y" for yes, anything else for no): ').lower().strip()
    if end_command == "y":
        game(wins, losses)

def main():
    num_wins = 0
    num_losses = 0

    game(num_wins, num_losses)

if __name__ == '__main__':
    main()
    