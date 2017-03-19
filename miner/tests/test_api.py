import json
import random
import logging
from django.test import TestCase, Client
from miner.models import Game
from miner.Board import Board, CLICK, DOUBLE_CLICK, FLAG


class CreateGameAPITest(TestCase):

    def setUp(self):
        self.client = Client()

    def testCreateGame(self):
        res = self.client.post(
            "/api/create/",
            json.dumps(dict(
                numOfMines=10,
                size=[10, 20]
            )),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 201)
        body = json.loads(res.content.decode("utf-8"))
        self.assertIn("gameId", body)

    def testShouldNotAllowGet(self):
        res = self.client.get("/api/create/")
        self.assertEqual(res.status_code, 405)

    def testShouldNotCreateGameWithoutRequiredData(self):
        res = self.client.post(
            "/api/create/",
            json.dumps(dict(
                numOfMines=10
            )),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)

    def testShouldNotCreateGameWithBadJson(self):
        res = self.client.post(
            "/api/create/",
            "[{\"a\": b}]",
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)

    def testShouldNotAllowNoneJson(self):
        res = self.client.post(
            "/api/create/",
            {"a": 1, "b": 2},
        )
        self.assertEqual(res.status_code, 415)


# Test miner.api.get_game
class GetGameAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        res = self.client.post(
            "/api/create/",
            json.dumps(dict(
                numOfMines=10,
                size=[10, 20]
            )),
            content_type="application/json"
        )
        body = json.loads(res.content.decode("utf-8"))
        self.game_id = body["gameId"]

    def testGetGame(self):
        res = self.client.get(
            "/api/game/{}".format(self.game_id)
        )
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode("utf-8"))
        self.assertIn("state", body)

    def testShouldReturn404(self):
        game_id = self.game_id + 100
        res = self.client.get(
            "/api/game/{}".format(game_id)
        )
        self.assertEqual(res.status_code, 404)


# Test miner.api.apply_action
class ApplyActionAPITest(TestCase):

    def setUp(self):
        self.client = Client()
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

    def testApplyAction(self):
        res = self.client.post(
            "/api/game/{}/action/".format(self.game.id),
            json.dumps(dict(
                action_type=CLICK,
                x=0,
                y=4,
            )),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(
            body["state"],
            [[None, None, None, 1, 0],
             [None, None, None, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
        res = self.client.post(
            "/api/game/{}/action/".format(self.game.id),
            json.dumps(dict(
                action_type=CLICK,
                x=0,
                y=2,
            )),
            content_type="application/json"
        )
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(
            body["state"],
            [[None, None, 1, 1, 0],
             [None, None, None, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )

    def testMalformedAction(self):
        res = self.client.post(
            "/api/game/{}/action/".format(self.game.id),
            json.dumps(dict(
                action_type=CLICK,
                x=0,
            )),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)


# Test miner.api.go_back
class GoBackAPITest(TestCase):

    def setUp(self):
        self.client = Client()
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

    def testGoBack(self):
        self.game.apply_action(CLICK, 0, 4)
        self.game.apply_action(CLICK, 0, 2)
        res = self.client.get(
            "/api/game/{}/back/".format(self.game.id),
        )
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(
            body["state"],
            [[None, None, None, 1, 0],
             [None, None, None, 2, 1],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )