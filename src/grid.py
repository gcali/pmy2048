#! /usr/bin/env python3

import random
import itertools
import sys

class GameOver(Exception):
    pass

class MoveNotValid(Exception):
    pass

class Grid:
    DIM = 4
    def __init__(self, seed:int=None):
        if seed != None:
            self.seed = seed
        else:
            self.seed = random.randint(0, sys.maxsize)

        self.random_generator = random.Random(self.seed)
        self._init_matrix()

    def dim_iterator(*args):
        for i in range(Grid.DIM):
            yield i

    def dim_reverse_iterator(*args):
        for i in range(Grid.DIM):
            yield (Grid.DIM -1 - i)

    def _get_move_line(self, direction:str, n:int) -> list:
        if direction in ["up", "u"]:
            line = [self._matrix[i][n] for i in self.dim_iterator()]
        elif direction in ["down", "d"]:
            line = [self._matrix[i][n] for i in self.dim_reverse_iterator()]
        elif direction in ["left", "l"]:
            line = [self._matrix[n][i] for i in self.dim_iterator()]
        elif direction in ["right", "r"]:
            line = [self._matrix[n][i] for i in self.dim_reverse_iterator()]
        else:
            raise ValueError
        return line

    def _set_move_line(self, direction:str, n:int, line):
        for i,e in enumerate(line):
            if direction in ["up", "u"]:
                self._matrix[i][n] = e
            elif direction in ["down", "d"]:
                self._matrix[Grid.DIM - 1 -i][n] = e
            elif direction in ["left", "l"]:
                self._matrix[n][i] = e
            elif direction in ["right", "r"]:
                self._matrix[n][Grid.DIM -1 -i] = e
            else:
                raise ValueError

    def _merge_line(self, line:list) -> list:
        new_line = list(line) 
        base = 0
        #print("Base:", base)
        for curr,e in enumerate(new_line):
            if e != 0:
                #print("Curr:", curr)
                for i in range(curr-1, base-1, -1):
                    #print("i:", i)
                    if new_line[i] != 0 and new_line[i] != e:
                        #print("First")
                        new_line[curr] = 0
                        new_line[i+1] = e
                        base = i+1
                        break
                    elif new_line[i] == e:
                        #print("Second")
                        new_line[curr] = 0
                        new_line[i] = 2 * e
                        base = i+1
                        break
                else:
                    new_line[curr] = 0
                    new_line[base] = e
        return new_line

    def _init_matrix(self):
        self._reset_matrix()
        for x,y in self.random_generator.sample(self._available_cells(), 2):
            self._matrix[x][y] = 2

    def _reset_matrix(self):
        self._matrix = [ [0 for x in range(Grid.DIM)] \
                            for y in range(Grid.DIM)  ]

    def move(self, direction:str):
        valid_move = False
        for n in self.dim_iterator():
            line = self._get_move_line(direction, n) 
            new_line = self._merge_line(line)
            if line != new_line:
                #print("Old: {}\nNew: {}".format(line, new_line))
                valid_move = True
            self._set_move_line(direction, n, new_line)
        if valid_move:
            available = self._available_cells()
            if not available:
                raise GameOver("Seed: {}".format(self.seed))
            else:
                x,y = self.random_generator.choice(available)
                self._matrix[x][y] = 2 if self.random_generator.randrange(10)\
                                       else 4
        return self

    def __str__(self) -> str:
        def remove_zeroes(row:list) -> list:
            return [ str(x) if x is not 0 else ' ' for x in row ]
        row_format = "|" + "{:^4}|"*Grid.DIM
        separator_line = "-" * (5 * Grid.DIM + 1)
        return "\n".join([separator_line] + list(itertools.chain(
            *zip( [row_format.format(*(remove_zeroes(row))) \
                   for row in self._matrix],
                   [separator_line] * len(self._matrix)))))

    def _available_cells(self) -> list:
        return [ (i,j)\
                for i in range(Grid.DIM)\
                    for j in range(Grid.DIM)\
                        if self._matrix[i][j] == 0 ]


    def test(self):
        self._matrix[0][0] = 2
        self._matrix[0][2] = 2
        self._matrix[1][2] = 2

if __name__ == '__main__':
    g = Grid()
    print(g)
    g.test()
    print(g)
        
