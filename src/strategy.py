#! /usr/bin/env python3 

from grid import Grid, GameOver
import random

def random_solutor(g:Grid):
    moves = ["up", "down", "left", "right"]
    move = random.choice(moves)
    while not g.is_move_valid(move):
        move = random.choice(moves)
    g.move(move)
    return move

def primitive_solutor(g:Grid):
    moves = ["up", "left", "right", "down"]
    for m in moves:
        if g.is_move_valid(m):
            move = m
            break
    else:
        move = "up"
    g.move(move)
    return move

def test_strategy_target(target, solutor):
    g = Grid()
    moves = []
    number_of_games = 1
    while not g.has_won(target):
        try:
            moves.append(solutor(g))
        except GameOver as e:
            number_of_games = number_of_games + 1
            if number_of_games % 500 == 0:
                printf("Haven't won after {} games".format(number_of_games))
            g = Grid()
    return number_of_games, moves
            
def print_separator():
    print("\n" + "-" * 20 + "\n")

def test_strategy(name:str, solutor:("Grid -> (move, Grid)")):
    print("Testing strategy {}".format(name))
    targets = [2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13]
    print("Targets to be checked: {}".format(",".join(
        [str(x) for x in targets])))
    print_separator()
    for t in targets:
        print("Checking target {}...".format(t))
        games,moves = test_strategy_target(t, solutor)
        print("Target {} met in {} games.".format(t, games))
        res = input("Procede to the next one? ".format(t))
        if res.lower() not in ["", "y", "yes", "s", "si"]:
            break
    return True

if __name__ == '__main__':
    test_strategy("Primitive", primitive_solutor)
