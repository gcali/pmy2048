#! /usr/bin/env python3 

from grid import Grid, GameOver
import random

_learning_solutor_moves = 10
def learning_solutor(g:Grid):
    moves = ["up", "down", "left", "right"]
    moves = [x for x in moves if g.is_move_valid(x)]
    scores = {}
    for m in moves:
        scores[m] = []
        for i in range(_learning_solutor_moves):
            g_sub = g.copy()
            local_score = g_sub.move(m)
            try:
                while not g_sub.has_won():
                    _,s = random_solutor(g_sub, True)
                    local_score = local_score + s
            except GameOver as e:
                pass
            scores[m].append(local_score)
        scores[m] = sum(scores[m])/len(scores[m])
    possibilities = [ (s,m) for (m,s) in scores.items() ]
    possibilities.sort()
    possibilities.reverse()
    print(possibilities)
    try:
        g.move(possibilities[0][1]) 
    except IndexError as e:
        print(e)
        print(possibilities)
        print(g)
        return "up"
    return possibilities[0][1]

def random_solutor(g:Grid, return_score=False):
    moves = ["up", "down", "left", "right"]
    move = random.choice(moves)
    while not g.is_move_valid(move):
        if not g.is_there_available_move():
            move = "up"
            break
        move = random.choice(moves)
    s = g.move(move)
    return move if not return_score else (move,s)

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
                print("Haven't won after {} games".format(number_of_games))
            g = Grid()
    return number_of_games, moves
            
def print_separator():
    print("\n" + "-" * 20 + "\n")

def test_strategy(name:str, solutor:("Grid -> (move, Grid)"),
                  targets=[2**6, 2**7, 2**8, 2**9, 2**10, 2**1, 2**12,
                           2**13], interactive=True):
    print("Testing strategy {}".format(name))
    print("Targets to be checked: {}".format(",".join(
        [str(x) for x in targets])))
    for i,t in enumerate(targets):
        print("Checking target {}...".format(t))
        games,moves = test_strategy_target(t, solutor)
        print("Target {} met in {} games.".format(t, games))
        if interactive and i != len(targets) - 1:
            res = input("Procede to the next one? ".format(t))
            if res.lower() not in ["", "y", "yes", "s", "si"]:
                break
        elif i == len(targets) - 1:
            break
    return True

if __name__ == '__main__':
    #test_strategy("Random", random_solutor, [64, 128], True)
    #test_strategy("Primitive", primitive_solutor, [256, 512], False)
    test_strategy("Learning", learning_solutor, [2048], True)
