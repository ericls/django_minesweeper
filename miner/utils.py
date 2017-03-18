# -*- coding: utf-8 -*-
import random
import itertools


class Board(object):

    def __init__(self, initial_board):
        row = len(initial_board)
        try:
            col = len(initial_board[0])
        except TypeError:
            raise ValueError('input board is malformed')
        if not all(map(lambda _: len(_) == col, initial_board)):
            raise ValueError('input board is malformed')
        self.size = (row, col)
        self.board = initial_board
        self.coordinates = [(i, j) for j in range(col) for i in range(row)]

    @classmethod
    def generate_new_board(cls, size, num_of_mines, seed=None):
        """
        Generate a new Board
        :param size: size of the board
        :param num_of_mines: number of mines to plant
        :param seed: the seed used in random module
        :return: a new `Board` instance, planted and marked
        """
        row, col = size
        num_of_cells = row * col
        if num_of_cells <= num_of_mines:
            raise ValueError('Number of cells should be greater than number of mines')
        empty_board = cls([[0 for _ in range(col)] for _ in range(row)])
        empty_board.plant(num_of_mines, seed)
        empty_board.mark()
        return empty_board

    def plant(self, num_of_mines, seed=None):
        """
        Mark the current board
        :param num_of_mines: number of mines to plant
        :param seed: the seed used in random module
        :return: None
        """
        flat = [item for sublist in self.board for item in sublist]
        if 9 in flat:
            raise RuntimeError('this board appears to be planted already')
        random.seed(seed)
        mine_coordinates = random.sample(self.coordinates, num_of_mines)
        for (x, y) in mine_coordinates:
            self.board[x][y] = 9

    def mark(self):
        """
        Mark the current board
        :return: None
        """
        for (x, y) in self.coordinates:
            self.__mark_one_cell((x, y))

    def __mark_one_cell(self, coordinate):
        x, y = coordinate
        if self.board[x][y] == 9:
            return
        adjacent_coordinates = self.__get_adjacent_cell_coordinates(coordinate)
        count = 0
        for (a, b) in adjacent_coordinates:
            if self.board[a][b] == 9:
                count += 1
        self.board[x][y] = count

    def __get_adjacent_cell_coordinates(self, coordinate):
        x, y = coordinate
        diff_list = [-1, 0, 1]
        adjacent_coordinates = set()
        deltas = itertools.product(diff_list, diff_list)
        for (i, j) in deltas:
            if (i, j) == (0, 0):
                continue
            a, b = x + i, y + j
            if (a, b) in self.coordinates:
                adjacent_coordinates.add((a, b))
        return list(adjacent_coordinates)

