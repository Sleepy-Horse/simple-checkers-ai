import enum
from copy import deepcopy

import numpy as np


def sign(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    return -1


def getNextColor(color):
    return int(color == 1) + 1


class Board:
    boards = [(np.ones((8, 8)), 1)]   # board -> win or lose

    def __init__(self):
        self.board = [[0 for j in range(8)] for i in range(8)]
        for i in range(4):
            for j in range(3):
                self.board[i * 2 + j % 2][j] = 1
                self.board[i * 2 + (j + 1) % 2][j + 5] = 2

    def get_all_possible_boards(self, color):
        b = []
        for turn in self.get_all_possible_turns(color):
            b.append(self.copy().turn(turn).board)
        return b


    def get_all_possible_turns(self, color):
        s = set()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0 or (self.board[i][j] != color):
                    continue
                s |= self.get_possible_turns((i, j))
        return s

    def get_possible_turns(self, pos):
        s = set()
        for x in (-1, 1):
            for y in (-1, 1):
                cell = self.get_cell((pos[0] + x, pos[1] + y))
                if cell == 0:
                    s.add((pos[0], pos[1], pos[0] + x, pos[1] + y))
                elif cell != 3 and cell != self.get_cell(pos) and self.get_cell((pos[0] + 2 * x, pos[1] + 2 * y)) == 0:
                    s.add((pos[0], pos[1], pos[0] + 2 * x, pos[1] + 2 * y))
        return s

    def get_cell(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= 8 or pos[1] >= 8:
            return 3

        return self.board[pos[0]][pos[1]]

    def turn(self, turn):
        x0, y0, x1, y1 = turn
        self.board[x1][y1] = self.board[x0][y0]
        self.board[x0][y0] = 0
        if abs(x0 - x1) + abs(y0 - y1) == 2:
            return self
        self.board[x0 + sign(x1 - x0)][y0 + sign(y1 - y0)] = 0
        return self

    def is_there_color(self, color):
        for i in range(8):
            for j in range(8):
                if color == self.board[i][j]:
                    return True
        return False

    def count_color(self, color):
        s = 0
        for i in range(8):
            for j in range(8):
                if color == self.board[i][j]:
                    s += 1
        return s

    def get_cells(self):
        cells = []
        for line in self.board:
            cells += line
        return cells

    def print_board(self):
        for line in self.board:
            print(*line)

    def checkers_amount(self):
        checkers = 0
        for line in self.board:
            checkers += 8 - line.count(0)
        return checkers

    def is_game_ended(self):
        return not (self.is_there_color(1) and self.is_there_color(2))

    def copy(self):
        board = Board()
        board.board = deepcopy(self.board)
        return board
