import time
import os
import random
import copy

try:
    import keyboard
except ImportError:
    input("The keyboard library is not installed. Please close the program (ctrl+c) and install it.")

settings = {
    "clear" : True,
    "loop" : False,
    "snake" : "S",
    "wall" : "N",
    "apple" : "A"
}

def print_stage(stage):
    # clears the terminal (can be changed in settings) then prints each tile of the stage
    if settings["clear"]:
        os.system("cls" if os.name == "nt" else "clear")
    for row in stage:
        for tile in row:
            print(tile, end = "")
        print()

def check_input(direction, snake):
    snake_head_y = int(snake[0][0])
    snake_head_x = int(snake[0][1])
    # this does an additional check to prevent colliding by immediately doubling back
    if (keyboard.is_pressed("w") or keyboard.is_pressed("up")) and (len(snake) == 1 or snake[1][0] != snake_head_y - 1):
        direction = "w"
    if (keyboard.is_pressed("s") or keyboard.is_pressed("down")) and (len(snake) == 1 or snake[1][0] != snake_head_y + 1):
        direction = "s"
    if (keyboard.is_pressed("a") or keyboard.is_pressed("left")) and (len(snake) == 1 or snake[1][1] != snake_head_x - 1):
        direction = "a"
    if (keyboard.is_pressed("d") or keyboard.is_pressed("right")) and (len(snake) == 1 or snake[1][1] != snake_head_x + 1):
        direction = "d"
    
    return direction

def moving(direction, snake, stage, app):
    # inserts a new link of the snake at the head based on new direction and sets the old tail for deletion, giving the appearance of movement
    # the old tail stays if an apple was eaten though, making the snake grow
    del_tail = None
    snake_head_y = int(snake[0][0])
    snake_head_x = int(snake[0][1])

    if direction == "w":
        snake.insert(0, (snake_head_y - 1, snake_head_x))
    if direction == "s":
        snake.insert(0, (snake_head_y + 1, snake_head_x))
    if direction == "a":
        snake.insert(0, (snake_head_y, snake_head_x - 1))
    if direction == "d":
        snake.insert(0, (snake_head_y, snake_head_x + 1))

    # if looping, sets the coordinate to the other side of the board instead of going into wall
    if settings["loop"]:
        # vertical looping
        if int(snake[0][0]) == 0:
            del snake[0]
            snake.insert(0, (len(stage) - 2, snake_head_x))
        if int(snake[0][0]) == len(stage) - 1:
            del snake[0]
            snake.insert(0, (1, snake_head_x))

        # horizontal looping
        if int(snake[0][1]) == 0:
            del snake[0]
            snake.insert(0, (snake_head_y, len(stage[0]) - 2))
        if int(snake[0][1]) == len(stage[0]) - 1:
            del snake[0]
            snake.insert(0, (snake_head_y, 1))

    if snake[0] != app:
        del_tail = snake.pop()
        app_gone = False
    else: 
        app_gone = True
    return snake, stage, app_gone, del_tail

def applize(stage, grid_x, grid_y):
    # places a random apple on the stage within the walls, avoiding where the snake is
    app_y = random.randint(1, grid_y - 2)
    app_x = random.randint(1, grid_x - 2)
    while stage[app_y][app_x] == settings["snake"]:
        app_y = random.randint(1, grid_y - 2)
        app_x = random.randint(1, grid_x - 2)

    stage[app_y][app_x] = settings["apple"]

    return stage, (app_y, app_x)

def set_stage(grid_x, grid_y):
    # initializes the stage, based on grid size
    wall_char = settings["wall"]
    top_bottom = [wall_char] * grid_x
    mid = [" "] * grid_x
    mid[0] = wall_char
    mid[grid_x - 1] = wall_char
    stage_matrix = [top_bottom]
    # creates deep copies because otherwise these are linked
    for i in range(grid_y - 2):
        stage_matrix.append(copy.deepcopy(mid))
    stage_matrix.append(copy.deepcopy(top_bottom))

    return stage_matrix

def game(x, y):
    grid_x = int(x) + 2
    grid_y = int(y) + 2
    # middle for starting position
    mid_x = grid_x // 2
    mid_y = grid_y // 2

    over = False
    frame_check = 0
    score = 0

    # snake coordinates are (y,x) to match the stage matrix
    snake_list = [(mid_y, mid_x)]

    stage_matrix = set_stage(grid_x, grid_y)
    stage_matrix[snake_list[0][0]][snake_list[0][1]] = settings["snake"]
    stage_matrix, app_tup = applize(stage_matrix, grid_x, grid_y)

    print_stage(stage_matrix)

    print()
    print("Press any arrow key or from wasd to begin!")
    print("It is highly recommended to click outside of the terminal (and code if run in an IDE) to prevent typing while pressing keys.")

    valid_directions = ["w", "a", "s", "d", "up", "left", "down", "right"]
    # waits for a valid direction input to start the game
    direction = keyboard.read_key()
    while direction not in valid_directions:
        direction = keyboard.read_key()
    if direction in valid_directions[4:]:
        if direction == "up":
            direction = "w"
        if direction == "left":
            direction = "a"
        if direction == "down":
            direction = "s"
        if direction == "right":
            direction = "d"

    while not over:
        # this game checks for input every 0.05 seconds, but only updates the board every 0.2 seconds
        # this is because <= 0.1s board updates are too fast and cause incomplete prints before they get reloaded 
        # (in the vscode terminal at least, the main terminal seems to print faster?)
        # while waiting 0.2s for checking input makes it way too unresponsive
        time.sleep(0.05)
        frame_check += 1

        direction = check_input(direction, snake_list)

        if frame_check == 4:
            snake_list, stage_matrix, app_gone, del_tail = moving(direction, snake_list, stage_matrix, app_tup)

            # builds the snake
            for segment in snake_list:
                stage_matrix[int(segment[0])][int(segment[1])] = settings["snake"]

            # if an apple was not consumed, delete the tail
            # extra check bc without it a segment wouldn't display if head immediately replaced where tail was
            if not app_gone and del_tail not in snake_list:
                stage_matrix[int(del_tail[0])][int(del_tail[1])] = " "

            # if an apple was consumed, create a new one and do nothing to the tail
            if app_gone:
                score += 1
                if len(snake_list) != (grid_x - 2) * (grid_y - 2):
                    stage_matrix, app_tup = applize(stage_matrix, grid_x, grid_y)

            # only show the stage after creating the new apple/removing the tail
            print_stage(stage_matrix)
            frame_check = 0

            # if the snake fills the board, it's a win
            if len(snake_list) == (grid_x - 2) * (grid_y - 2):
                over = True
                print("You win!")
            # detects if the snake collides with the upper or lower wall
            if int(snake_list[0][0]) == 0 or int(snake_list[0][0]) == grid_y - 1:
                over = True
                print("Death by wall")
            # detects if the snake collides with the side walls
            if int(snake_list[0][1]) == 0 or int(snake_list[0][1]) == grid_x - 1:
                over = True
                print("Death by wall")
            # detects is the snake collides with itself
            if snake_list[0] in snake_list[1:]:
                over = True
                print("Stop hitting yourself")
    # the score system could be more interesting tbh, right now it just counts the number of apples eaten
    # a different version could factor in time, or at least start at 1 so it looks more presentable
    print(f'Score: {score}')

    end_command = input('Type "replay" to play the same stage, "return" to go back to menu, or "stop" to close: ').lower().strip()
    
    end_commands = ["replay", "return", "stop"]
    while end_command not in end_commands:
        end_command = input('Please type "replay" to play the same stage, "return" to go back to menu, or "stop" to close: ').lower().strip()

    if end_command == "replay":
        game(x, y)
    if end_command == "return":
        main()
    if end_command == "stop":
        return
    
def settings_screen():
    global settings
    print()
    print("            Settings")
    print(f"Clear terminal between frames: {settings['clear']}")
    print(f"      Loop at walls: {settings['loop']}")
    print(f"       Snake character: {settings['snake']}")
    print(f"        Wall character: {settings['wall']}")
    print(f"       Apple character: {settings['apple']}")
    print()
    print('Enter which setting you would like to change, or "return" to go back to title screen: ')
    print('"clear", "loop", "snake", "wall", "apple", "return"')
    to_edit = input().lower().strip()

    while to_edit != "return" and to_edit not in settings:
        to_edit = input("That is not an accepted input, please type one of the given settings: ").lower().strip()

    if to_edit == "clear":
        settings["clear"] = not settings["clear"]

    if to_edit == "loop":
        settings["loop"] = not settings["loop"]

    if to_edit == "snake":
        snake_set = input("Enter what character you would like to replace the snake segments with: ").strip()
        while len(snake_set) != 1:
            snake_set = input("Please enter one character to represent snake segments: ")
        settings["snake"] = snake_set

    if to_edit == "wall":
        wall_set = input("Enter what character you would like to replace the wall with: ").strip()
        while len(wall_set) != 1:
            wall_set = input("Please enter one character to represent the wall: ")
        settings["wall"] = wall_set

    if to_edit == "apple":
        app_set = input("Enter what character you would like to replace the apple with: ").strip()
        while len(app_set) != 1:
            app_set = input("Please enter one character to represent the apple: ")
        settings["apple"] = app_set

    if to_edit == "return":
        return
        
    settings_screen()

def title():
    # so, there is a better way to print whole sections using triple quotes, but the indents get messy
    # and the obvious workaround with a certain library apparently left aligns all text
    # no idea if this would affect the spaces I use to center the text, but I don't feel like restructuring to find out
    # also there's a way to add spaces without typing them in the strings themselves, I didn't learn of this until everything was done
    print()
    print("         Terminal Snake")
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
        ret_x, ret_y = title()
        return ret_x, ret_y
    
    if command == "help":
        print()
        print("This is Terminal Snake, a version of Snake playable in the terminal.")
        print("Arrow keys and wasd can be used to control the snake, represented by an S.")
        print("The goal of the game is to collect as many apples (A) as possible, while avoiding walls (N).")
        print("After entering play, you will be prompted to specify the board dimensions.")
        print("The default is 16x8, but you can input a custom size.")
        print("If specifying your own board size, keep in mind that the spaces between rows are wider")
        print("than between characters, so the depth of the board will be over-represented.")
        print("Some aspects of the gameplay may be changed in the settings.")
        print("The board may flash rapidly as it is cleared and reprinted,")
        print("so be careful if you are sensitive to flashing lights.")
        print("Like anything in the terminal, the program can be ended at any point by pressing ctrl+c.")
        input("Once you are done reading this, press enter. ")
        ret_x, ret_y = title()
        return ret_x, ret_y

    if command == "play":
        print()
        print("What board size would you like?")
        board_size = input('Enter either "default" or numbers in the form "x y": ').lower().split()
        print(board_size)
        # checks 3 input cases: 1. the input is a single string that isn't "default"
        while ((len(board_size) == 1 and board_size[0] != "default") or 
            # 2. the input is multiple strings that aren't ints
            (len(board_size) == 2 and (not board_size[0].isdigit() or not board_size[1].isdigit())) or
            # 3. the input is more than 2 strings
            (len(board_size) > 2)):
                board_size = input('Please enter either "default" or positive integers in the form "x y": ').lower().split()

        # ensures custom board size isn't too small 
        while (len(board_size) == 2 and 
            ((int(board_size[0]) < 1 or int(board_size[1]) < 1) or 
            (int(board_size[0]) < 2 and int(board_size[1]) < 2))):
                print("If entering a custom size, ensure neither length is 0 and that at least one length is >1.")
                board_size = input('Please enter either "default" or positive integers in the form "x y": ').lower().split()
    
        if board_size[0] == "default":
            return 16, 8
        else:
            return board_size[0], board_size[1]


def main():
    ori_x, ori_y = title()

    game(ori_x, ori_y)

if __name__ == "__main__":
    main()