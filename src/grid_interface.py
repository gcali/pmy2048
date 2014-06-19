#! /usr/bin/env python3

from grid import *
import interface
import curses
from interface import Window
import sys
from math import log

_WORD_DIM = 5
_CELL_DIM = 3 + _WORD_DIM #space for the word, margins and a separator
def create_window_from_grid(g:Grid):
    win = Window(1 + 4 * (Grid.DIM), 2 + _CELL_DIM * Grid.DIM)
    for i in range(win.dim_row):
        if i % 4 == 0:
            regular_char = interface.get_constant("hline")
            if i == 0:
                left_char = interface.get_constant("ulcorner")
                right_char = interface.get_constant("urcorner")
                intersection_char = interface.get_constant("inter_down")
            elif i == win.dim_row - 1:
                left_char = interface.get_constant("dlcorner")
                right_char = interface.get_constant("drcorner")
                intersection_char = interface.get_constant("inter_up")
            else:
                left_char = interface.get_constant("inter_right")
                right_char = interface.get_constant("inter_left")
                intersection_char = interface.get_constant("cross")
            for col in range(win.dim_col-1):
                if col == 0:
                    win.print_special_character(i,col,left_char)
                elif col == win.dim_col - 2:
                    win.print_special_character(i,col,right_char)
                elif col % _CELL_DIM == 0:
                    win.print_special_character(i,col,intersection_char)
                else:
                    win.print_special_character(i,col,regular_char)
        else:
            regular_char = curses.ACS_VLINE
            #TODO Simplify a little
            for col in range(0, win.dim_col):
                if col % _CELL_DIM == 0:
                    win.print_special_character(i,col,regular_char)
                elif col % _CELL_DIM == 1 or\
                     col % _CELL_DIM == (_WORD_DIM + 3) -1:
                    win.print_str(i,col,' ')
                elif i % 4 == 1 or i % 4 == 3:
                    win.print_str(i,col,' ' * _WORD_DIM)
                elif col % _CELL_DIM == 2:
                    win.print_str(i,col,' ' * _WORD_DIM)
                    x = (i - 2)//4
                    y = (col - 2) // _CELL_DIM
                    n = g._matrix[x][y]
                    attr = curses.color_pair(0)
                    if n == 0:
                        n = ' '
                    else:
                        l = int(log(n, 2))
                        if l <= 6:
                            attr = curses.color_pair(l)
                        else:
                            attr = curses.color_pair(l%6) | curses.A_BOLD
                    format_string = "{{:^{}}}".format(_WORD_DIM)
                    n_string = format_string.format(n)
                    win.print_str(i,col,n_string, attr)
    win.refresh()
    return win

if __name__ == '__main__':
    interface.start()
    g = Grid()
    w = create_window_from_grid(g)
    w.get_char()
    interface.close()
    print(g)


