#! /usr/bin/env python3

from grid import *
import interface
import curses
from interface import Window
import sys
from math import log

_WORD_DIM = 5
def create_window_from_grid(g:Grid):
    win = Window(1 + 4 * (Grid.DIM), 2 + (3 + _WORD_DIM) * (Grid.DIM))
    for i in range(win.dim_row):
        if i % 4 == 0:
            regular = curses.ACS_HLINE
            if i == 0:
                left = curses.ACS_ULCORNER
                right = curses.ACS_URCORNER
                intersection = curses.ACS_TTEE
            elif i == win.dim_row - 1:
                left = curses.ACS_LLCORNER
                right = curses.ACS_LRCORNER
                intersection = curses.ACS_BTEE
            else:
                left = curses.ACS_LTEE
                right = curses.ACS_RTEE
                intersection = curses.ACS_PLUS
            #win.print_special_character(i,0, curses.ACS_ULCORNER)
            for col in range(win.dim_col-1):
                if col == 0:
                    win.print_special_character(i,col,left)
                elif col == win.dim_col - 2:
                    win.print_special_character(i,col,right)
                elif col % (_WORD_DIM + 3) == 0:
                    win.print_special_character(i,col,intersection)
                else:
                    win.print_special_character(i,col,regular)
        else:
            regular = curses.ACS_VLINE
            for col in range(0, win.dim_col):
                if col % (_WORD_DIM + 3) == 0:
                    win.print_special_character(i,col,regular)
                elif col % (_WORD_DIM + 3) == 1 or\
                     col % (_WORD_DIM + 3) == (_WORD_DIM + 3) -1:
                    win.print_str(i,col,' ')
                elif i % 4 == 1 or i % 4 == 3:
                    win.print_str(i,col,' ' * _WORD_DIM)
                elif col % (_WORD_DIM + 3) == 2:
                    win.print_str(i,col,' ' * _WORD_DIM)
                    x = (i - 2)//4
                    y = (col - 2) // (_WORD_DIM + 3)
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

