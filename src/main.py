#! /usr/bin/env python3 

from grid import Grid
import interface
from interface import Window
from grid_interface import create_window_from_grid

def start_game():
    while True:
        choice,key = menu()
        if key == "q" or\
           key == "x" or\
           key == "F3":
            return "Quit"
        elif key == "\n":
            if choice != 0:
                return "Quit"
            return start_new_game()

def menu():
    return interface.get_choice("Welcome to 2048 ncurses version",
                      ["New game", "Help", "Options", "Quit"])

def start_new_game():
    g = Grid()
    while True:
        has_to_exit = False
        w = create_window_from_grid(g)
        while True:
            c = w.get_char()
            if c == "KEY_UP" or\
               c == "k":
                direction = "up"
                break
            elif c == "KEY_DOWN" or\
                 c == "j":
                direction = "down"
                break
            elif c == "KEY_LEFT" or\
                 c == "h":
                direction = "left"
                break
            elif c == "KEY_RIGHT" or\
                 c == "l":
                direction = "right"
                break
            elif c == "q":
                has_to_exit = True
        if has_to_exit:
            return "Quit"
        try:
            g.move(direction)
        except GameOver as e:
            w.get_char()
            return "Game over"
        if g.has_won():
            return "Won"
            
if __name__ == '__main__':
    interface.start()
    result = start_game()
    interface.close()
    print(result)
