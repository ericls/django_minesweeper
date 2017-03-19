# -*- coding: utf-8 -*-
import random
import itertools

CLICK = 0
DOUBLE_CLICK = 1
FLAG = 2

GameActionTypes = [
    CLICK,
    DOUBLE_CLICK,
    FLAG
]


class Board(object):

    def __init__(self, initial_board, initial_state=None):
        row = len(initial_board)
        try:
            col = len(initial_board[0])
        except TypeError:
            raise ValueError('input board is malformed')
        if not all(map(lambda _: len(_) == col, initial_board)):
            raise ValueError('input board is malformed')
        self.size = (row, col)
        self.board = initial_board
        self.state = initial_state or [[None for _ in range(col)] for _ in range(row)]
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
        board = cls([[0 for _ in range(col)] for _ in range(row)])
        board.plant(num_of_mines, seed)
        board.mark()
        return board

    @property
    def mines_left(self):
        num_of_flags = [item for sublist in self.state for item in sublist].count(9)
        num_of_mines = [item for sublist in self.board for item in sublist].count(9)
        return num_of_mines - num_of_flags

    @property
    def win(self):
        return self.board == self.state

    @property
    def lost(self):
        return any([(10 in row) for row in self.state])

    def apply_action(self, t, x, y):
        """
        Apply action to the current board.
        This method mutates the `state` property.
        :param t: CLICK | DOUBLE_CLICK | FLAG
        :param x: coordinate X
        :param y: coordinate Y
        :return: (action_is_valid, new_state)
        """
        if self.win or self.lost:
            return False, self.state
        action_is_valid = None
        if t == CLICK:
            action_is_valid = self._apply_click(x, y)
        if t == DOUBLE_CLICK:
            action_is_valid = self._apply_double_click(x, y)
        if t == FLAG:
            action_is_valid = self._apply_flag(x, y)
        return action_is_valid, self.state

    def plant(self, num_of_mines, seed=None):
        """
        Mark the current board.
        This method mutates the `board` property
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
        Mark the number of adjacent mines of each cell.
        :return: None
        """
        for (x, y) in self.coordinates:
            if self.board[x][y] == 9:
                for (a, b) in self.__get_adjacent_cell_coordinates((x, y)):
                    if not self.board[a][b] == 9:
                        self.board[a][b] += 1

    def _apply_click(self, x, y):
        """
        Applies CLICK action to the current board, on cell (x, y).
        :param x: coordinate X
        :param y: coordinate Y
        :return: True if the action is successfully applied
        """
        state_cell_value = self.state[x][y]
        if state_cell_value is not None:
            return False
        cell_value = self.board[x][y]
        if cell_value == 9:
            self.state[x][y] = 10
            return True
        if 0 < cell_value < 9:
            self.state[x][y] = cell_value
            return True
        self.state[x][y] = 0
        adjacent_cells_coordinates = self.__get_adjacent_cell_coordinates((x, y))
        for (a, b) in adjacent_cells_coordinates:
            self._apply_click(a, b)
        return True

    def _apply_double_click(self, x, y):
        """
        Applies DOUBLE_CLICK action to the current board, on cell (x, y).
        A DOUBLE_CLICK clicks all adjacent cells if the value of the clicked cell is equal to
        the number of adjacent flags
        :param x: coordinate X
        :param y: coordinate Y
        :return: True if the action is successfully applied
        """
        state_cell_value = self.state[x][y]
        if not state_cell_value:
            return False
        adjacent_cells_coordinates = self.__get_adjacent_cell_coordinates((x, y))
        adjacent_flag_count = 0
        for (a, b) in adjacent_cells_coordinates:
            if self.state[a][b] == 9:
                adjacent_flag_count += 1
        if adjacent_flag_count != state_cell_value:
            return False
        for (a, b) in adjacent_cells_coordinates:
            if not self.state[a][b] == 9:
                self._apply_click(a, b)
        return True

    def _apply_flag(self, x, y):
        """
        Applies FLAG action to the current board, on cell (x, y).
        It sets or removes a flag at the cell.
        :param x: coordinate X
        :param y: coordinate Y
        :return: True if the action is successfully applied
        """
        if self.state[x][y] == 9:
            self.state[x][y] = None
            return True
        if self.state[x][y]:
            return False
        if not self.mines_left > 0:
            return False
        self.state[x][y] = 9
        return True

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
        return adjacent_coordinates
