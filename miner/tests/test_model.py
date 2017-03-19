import json
import random
import logging
from django.test import TestCase, Client
from miner.models import Game
from miner.Board import Board, CLICK, DOUBLE_CLICK, FLAG


class GameModelTest(TestCase):

    def setUp(self):
        initial_field_data = [
            [0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0],
            [0, 0, 0, 0, 9],
            [0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board = Board(initial_field_data)
        board.mark()
        self.marked_initial_data = board.board
        self.game = Game.objects.create(board=json.dumps(self.marked_initial_data))

    def testReadGameAndParseBoardData(self):
        game = Game.objects.get(pk=self.game.pk)
        self.assertEqual(
            json.loads(game.board),
            self.marked_initial_data
        )

    def testApplyActionAndLatestState(self):
        game = Game.objects.get(pk=self.game.pk)
        game.apply_action(CLICK, 0, 4)
        game.apply_action(CLICK, 0, 2)
        game.apply_action(FLAG, 1, 2)
        game.apply_action(DOUBLE_CLICK, 0, 2)
        self.assertEqual(
            game.latest_state["state"],
            [[None, 1, 1, 1, 0],
             [None, 1, 9, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )

    def testGoBack(self):
        game = Game.objects.get(pk=self.game.pk)
        game.apply_action(CLICK, 0, 4)
        game.apply_action(CLICK, 0, 2)
        game.apply_action(FLAG, 1, 2)
        game.apply_action(DOUBLE_CLICK, 0, 2)
        game.apply_action(DOUBLE_CLICK, 1, 1)
        self.assertEqual(
            game.latest_state["state"],
            [[0, 1, 1, 1, 0],
             [0, 1, 9, 2, 1],
             [1, 2, 2, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        game.go_back()
        self.assertEqual(
            game.latest_state["state"],
            [[None, 1, 1, 1, 0],
             [None, 1, 9, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )