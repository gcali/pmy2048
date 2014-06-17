#! /usr/bin/env python3 

import curses
from grid import Grid, GameOver
import interface
from interface import Window
from grid_interface import create_window_from_grid
import sys

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
    score = 0
    while True:
        has_to_exit = False
        w = create_window_from_grid(g)
        score_win = w.create_next_to(3,7)
        score_win.print_str(0,0,"Score")
        score_win.refresh()
        while True:
            score_win.print_str(1,0," "*7)
            score_win.print_str(1,0,"{:>7}".format(score),\
                                curses.color_pair(5) | curses.A_BOLD)
            score_win.refresh()
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
                break
        if has_to_exit:
            return "Quit"
        try:
            move_score = g.move(direction)
            score = score + move_score
            #print("Move score: {}".format(move_score), file=sys.stderr)
        except GameOver as e:
            res_win = w.create_under(1)
            res_win.print_str("You lost...", curses.color_pair(1) |\
                                             curses.A_BOLD)
            res_win.refresh()
            w.get_char()
            return "Game over"
        if g.has_won():
            res_win = w.create_under(1)
            res_win.print_str("You won!", curses.color_pair(3) |\
                                          curses.A_BOLD)
            res_win.refresh()
            w.get_char()
            return "Won"
            
if __name__ == '__main__':
    interface.start()
    result = start_game()
    interface.close()
    print(result)
