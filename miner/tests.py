import json
import random
from django.test import TestCase
from miner.models import Game
from miner.utils import Board, CLICK, DOUBLE_CLICK, FLAG


# Test miner.models.Game
class GameModelTest(TestCase):

    def setUp(self):
        initial_field_data = [
            [0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0],
            [0, 0, 0, 0, 9],
            [0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.initial_field_data = initial_field_data
        self.game = Game.objects.create(board=json.dumps(initial_field_data))

    def testReadGameAndParseBoardData(self):
        game = Game.objects.get(pk=self.game.pk)
        self.assertEqual(
            json.loads(game.board),
            self.initial_field_data
        )


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

    def testApplyActionToChangeStateEndToEnd(self):
        board = Board(self.initial_field_data)
        board.mark()
        board.apply_action(CLICK, 0, 4)
        self.assertEqual(
            board.state,
            [[None, None, None, 1, 0],
             [None, None, None, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(CLICK, 0, 2)
        self.assertEqual(
            board.state,
            [[None, None, 1, 1, 0],
             [None, None, None, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(FLAG, 1, 2)
        self.assertEqual(
            board.state,
            [[None, None, 1, 1, 0],
             [None, None, 9, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(FLAG, 0, 3)
        self.assertEqual(
            board.state,
            [[None, None, 1, 1, 0],
             [None, None, 9, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        res = board.apply_action(FLAG, 1, 2)
        self.assertEqual(res, False)
        self.assertEqual(
            board.state,
            [[None, None, 1, 1, 0],
             [None, None, None, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(FLAG, 1, 2)
        board.apply_action(DOUBLE_CLICK, 0, 2)
        self.assertEqual(
            board.state,
            [[None, 1, 1, 1, 0],
             [None, 1, 9, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(DOUBLE_CLICK, 1, 1)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(CLICK, 2, 3)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, 2, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(FLAG, 2, 4)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, 2, 9],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        board.apply_action(DOUBLE_CLICK, 2, 3)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, 2, 9],
             [None, None, 1, 1, 1],
             [None, None, None, None, None]]
        )
        board.apply_action(DOUBLE_CLICK, 3, 4)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, 2, 9],
             [None, None, 1, 1, 1],
             [None, None, 1, 0, 0]]
        )
        board.apply_action(FLAG, 3, 1)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, 2, 9],
             [None, 9, 1, 1, 1],
             [None, None, 1, 0, 0]]
        )
        board.apply_action(CLICK, 4, 0)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, 2, 9],
             [None, 9, 1, 1, 1],
             [1, None, 1, 0, 0]]
        )
        board.apply_action(DOUBLE_CLICK, 4, 0)
        self.assertEqual(
            board.state,
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, 2, 9],
             [1, 9, 1, 1, 1],
             [1, 1, 1, 0, 0]]
        )
        self.assertEqual(board.win, True)

