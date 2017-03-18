import random
from django.test import TestCase
from miner.utils import Board


# Test miner.utils.Board
class UtilsBoardTest(TestCase):

    def setUp(self):
        self.seed = random.random()
        initial_field_data = Board.generate_new_board((5, 5), 0, self.seed).board
        initial_field_data[1][2] = 9
        initial_field_data[2][4] = 9
        initial_field_data[3][1] = 9
        self.initial_field_data = initial_field_data

    def testGeneratingBoardWithGivenSeed(self):
        """
        Generated board should be the same when given the same seed.
        """
        round1 = Board.generate_new_board((10, 5), 10, self.seed).board
        round2 = Board.generate_new_board((10, 5), 10, self.seed).board
        self.assertEqual(round1, round2)

    def testGenerateRightNumberOfMine(self):
        """
        Generate_new_board should plant right amount of mines
        """
        board = Board.generate_new_board((10, 5), 10, self.seed).board
        flat = [item for sublist in board for item in sublist]
        self.assertEqual(flat.count(9), 10)

    def testPlantAlreadyPlantedMineField(self):
        """
        Should raise exception when plant already planted board
        """
        with self.assertRaises(RuntimeError):
            board = Board(self.initial_field_data)
            board.plant(10)

    def testGeneratingMoreMineThanCell(self):
        """
        Should raise exception when num_of_mine >= number of cells
        """
        with self.assertRaises(ValueError):
            Board.generate_new_board((10, 5), 50)

    def testMalformedInput(self):
        """
        Should raise exception when input is malformed
        """
        with self.assertRaises(ValueError):
            Board([1, [1]])
        with self.assertRaises(ValueError):
            Board([[1], [1, 2]])

    def testMarkBoard(self):
        """
        Should correctly mark a planted board
        """
        expected = [
            [0, 1, 1, 1, 0],
            [0, 1, 9, 2, 1],
            [1, 2, 2, 2, 9],
            [1, 9, 1, 1, 1],
            [1, 1, 1, 0, 0]
        ]
        board = Board(self.initial_field_data)
        board.mark()
        self.assertEqual(Board(self.initial_field_data).board, expected)
