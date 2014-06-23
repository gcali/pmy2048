#! /usr/bin/env python3 

from grid import Grid, GameOver
import interface
from interface import Window
from grid_interface import create_window_from_grid
import sys

score_digits = 7

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
                      #["New game", "Help", "Options", "Quit"])
                       ["New game", "Quit"])

def create_main_window_and_score(g:Grid) -> (Window,Window):
    main_window = create_window_from_grid(g)
    score_window = main_window.create_next_to(3,score_digits)
    score_window.print_str(0,0,"{{:>{}}}".format(\
        score_digits).format("Score"))
    refresh_score(score_window, 0)
    return main_window,score_window

def refresh_score(w:Window, s:"score"):
    w.print_str(1,0," "*score_digits)
    w.print_str(1,0,"{{:>{}}}".format(score_digits).format(s),\
                    interface.get_color("blue") | \
                    interface.get_constant("bold"))
    w.refresh()

def result_screen(w:Window,result:str):
    wait = True
    if result == "won":
        result = "You won! Do you want to go on? [y/n]"
        attr = interface.get_color("green") |\
               interface.get_constant("bold")
        wait = False
    elif result == "lost":
        result = "You lost..."
        attr = interface.get_color("red") |\
               interface.get_constant("bold")
    else:
        attr = interface.get_color("magenta") |\
               interface.get_constant("bold")
    w_result = w.create_under(1)
    w_result.print_str(result, attr)
    w_result.refresh()
    if wait:
        w_result.get_char() 
    return w_result

def start_new_game():
    g = Grid()
    score = 0
    w_main,w_score = create_main_window_and_score(g)
    target = 2048
    while True:
        has_to_exit = False
        while True:
            c = w_main.get_char()
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
                break
        if has_to_exit:
            return "Quit"
        try:
            move_score = g.move(direction)
            score = score + move_score
            w_main = create_window_from_grid(g)
            refresh_score(w_score, score)
        except GameOver as e:
            result_screen(w_main,"lost")
            return "Game over"
        if g.has_won(target):
            w_res = result_screen(w_main,"won")
            while True:
                c = w_main.get_char()
                if c == 'y' or c == 'n':
                    break
            if c == "n":
                return "Won"
            else:
                target = target * 2
                w_res.clear()
                w_res.refresh()
            
if __name__ == '__main__':
    interface.start()
    result = start_game()
    interface.close()
    print(result)
