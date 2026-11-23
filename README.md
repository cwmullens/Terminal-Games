# Terminal Games
by cwmullens  

A small collection of games playable in the terminal using Python.
## Description
**Photosensitivity warning: Snake updates the terminal rapidly, which causes the screen to flicker.**  
To use, open the directory and run main.py, which accesses the three games within game_code and allows them to be selected in a main menu. Each of the games can also be run individually without being called through main. The games included are:
### Snake
A customizable form of Snake where you control a snake that eats apples to grow larger while avoiding hitting walls and itself.
### Hangman
A guessing game where you guess letters or the full answer of a hidden phrase or word. Includes several difficulties, giving harder phrases and fewer guesses.
### Monty Hall
A short simulation of the famous Monty Hall problem where you guess a door you think has the prize and then are given the option to switch doors after seeing a door that the prize is *not* behind.
## Dependencies
All of the dependencies come within the modern Python standard library, so no downloads are necessary, but for bookkeeping they are:
- *os* 
- *random*
- *string*
- *json*
- *pathlib*
- *time*
- *copy*
- *keyboard*

Note not all games require all of these dependencies. Also, this project was originally developed on Windows, but **the *keyboard* module does not work properly on all operating systems, so Snake may not be playable.**  
For additional bookkeeping, it was built using Python version **3.14.6**.
## Navigation
Each game and the main menu require typing in commands, so they must be navigated with some precision. Each game also has a *help* option to understand how to play, as well as a *settings* option to modify the experience.  
## Limitations  
As mentioned above, the *keyboard* module does not work with all operating systems. Another limitation within Snake is that the box size can be set to larger than the terminal shows continuously, splitting the frame across multiple lines, though it still functions. Unlike the other two games, Snake also needs to update the screen constantly, which can have some side effects, such as the terminal clearing the screen between frames and some inputs potentially being missed if they fall between when the keyboard is checked.  

Within Hangman, there are only so many words and phrases within the word bank. By default, the game will not show repeats until all of them have been covered. However, adding more replayability is as easy as modifying *word_banks/hangman_bank.json*.
