#! /usr/bin/env python3

import random
import itertools
import sys

l = [4, 256, 16, 2,
     2, 64, 128, 4,
     8, 16, 32, 1024,
     4, 2, 512, 8]

class GameOver(Exception):
    pass

class MoveNotValid(Exception):
    pass

class Grid:

    DIM = 4
    DIRECTIONS = ["up", "down", "left", "right"]

    def __init__(self, seed:int=None, start=None):
        if seed != None:
            self.seed = seed
        else:
            self.seed = random.randint(0, sys.maxsize) 

        self.random_generator = random.Random(self.seed)
        if not start:
            self._init_matrix()
        else:
            self._init_matrix_from_list(start)

    def iterator_over_dim(*args):
        for i in range(Grid.DIM):
            yield i

    def iterator_over_dim_reversed(*args):
        for i in range(Grid.DIM - 1, -1, -1):
            yield i
            #yield (Grid.DIM -1 - i)

    def has_won(self, target:int=2048) -> bool:
        for i in range(Grid.DIM):
            for j in range(Grid.DIM):
                if self._matrix[i][j] == target:
                    return True
        return False

    def _get_move_line(self, direction:str, n:int) -> list:
        if direction in ["up", "u"]:
            line = [self._matrix[i][n] for i in \
                                       self.iterator_over_dim()]
        elif direction in ["down", "d"]:
            line = [self._matrix[i][n] for i in \
                                       self.iterator_over_dim_reversed()]
        elif direction in ["left", "l"]:
            line = [self._matrix[n][i] for i in \
                                       self.iterator_over_dim()]
        elif direction in ["right", "r"]:
            line = [self._matrix[n][i] for i in \
                                       self.iterator_over_dim_reversed()]
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
        score = 0
        for curr,e in enumerate(new_line):
            if e != 0:
                for i in range(curr-1, base-1, -1):
                    if new_line[i] != 0 and new_line[i] != e:
                        new_line[curr] = 0
                        new_line[i+1] = e
                        base = i+1
                        break
                    elif new_line[i] == e:
                        new_line[curr] = 0
                        new_line[i] = 2 * e
                        base = i+1
                        score = score + 2 * e
                        break
                else:
                    new_line[curr] = 0
                    new_line[base] = e
        return (new_line, score)

    def _init_matrix(self):
        self._reset_matrix()
        for x,y in self.random_generator.sample(self._available_cells(), 2):
            self._matrix[x][y] = 2

    def _init_matrix_from_list(self, l:list):
        self._reset_matrix()
        d = len(self._matrix)
        for i in range(d):
            for j in range(d):
                self._matrix[i][j] = l[d*i + j]

    def _reset_matrix(self):
        self._matrix = [ [0 for x in range(Grid.DIM)] \
                            for y in range(Grid.DIM)  ]

    def is_there_available_move(self) -> bool:
        is_there = False
        for d in Grid.DIRECTIONS:
            if self.is_move_valid(d):
                is_there = True
                break
        return is_there

    def move(self, direction:str):
        valid_move = False
        score = 0
        for n in self.iterator_over_dim():
            line = self._get_move_line(direction, n) 
            new_line,line_score = self._merge_line(line)
            score = score + line_score
            if line != new_line:
                valid_move = True
            self._set_move_line(direction, n, new_line)
        available = self._available_cells()
        #if not available and not self.is_there_available_move():
        #    raise GameOver("Seed: {}".format(self.seed))
        if valid_move:
            x,y = self.random_generator.choice(available)
            self._matrix[x][y] = 2 if self.random_generator.randrange(10)\
                                   else 4
        if not self._available_cells() and \
           not self.is_there_available_move():
            raise GameOver("Seed: {}".format(self.seed))
        return score

    #def is_move_valid(self, direction:str):
    #    for n in self.iterator_over_dim():
    #        line = self._get_move_line(direction, n)
    #        new_line,_score = self._merge_line(line)
    #        if line != new_line:
    #            return True
    #    return False
    def is_move_valid(self, direction:str):
        for n in self.iterator_over_dim():
            found_zero = False
            line = self._get_move_line(direction, n)
            for i in range(len(line)):
                e = line[i]
                if e == 0:
                    found_zero = True
                elif found_zero:
                    return True
                elif i != len(line) -1 and line[i] == line[i+1]:
                    return True
        return False

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
        v = 1
        for i in range(Grid.DIM):
            for j in range(Grid.DIM):
                self._matrix[i][j] = v
                v = v + 1
        self._matrix[Grid.DIM -1][Grid.DIM -1] = 0

    def copy(self):
        g = Grid()
        g._matrix = [ [ self._matrix[i][j]\
                        for j in range(len(self._matrix[i])) ]\
                            for i in range(len(self._matrix)) ]
        return g
                

if __name__ == '__main__':
    g = Grid()
    #g.test()
    print(g)
    g_1 = g.copy()
    g.move("up")
    print("Original after up:")
    print(g)
    print("Copy:")
    print(g_1)
    l = [4, 256, 16, 2,
         2, 64, 128, 4,
         8, 16, 32, 1024,
         4, 2, 512, 8]
    print("From list", l)
    print(Grid(start=l))
        
        

