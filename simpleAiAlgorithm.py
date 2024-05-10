import random

import Board

''' This algorithm just check all possibilities in 1 turn
    it checks which checkers can it attack and protect and randomly choose the best variant
'''
def best_turn(board, color):
    s = {0: set(), 1: set(), 2: set()}
    potential_enemy_turns = filter(lambda t: abs(t[0] - t[2]) == 2,
                                   list(board.get_all_possible_turns(Board.getNextColor(color))))
    potential_killed_cells = list(map(lambda t: ((t[0] + t[2]) / 2, (t[1] + t[3]) / 2), potential_enemy_turns))
    for my_turn in board.get_all_possible_turns(color):
        score = abs(my_turn[0] - my_turn[2]) == 2 + ((my_turn[:2]) in potential_killed_cells)
        s[score].add(my_turn)
    if len(s[2]) > 0:
        max_score = 2
    elif len(s[1]) > 0:
        max_score = 1
    else:
        max_score = 0
    return random.choice(tuple(s[max_score]))