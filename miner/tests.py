import json
import random
import logging
from django.test import TestCase, Client
from miner.models import Game
from miner.Board import Board, CLICK, DOUBLE_CLICK, FLAG

logging.disable(logging.CRITICAL)
CLICK_TYPE, DOUBLE_CLICK_TYPE, FLAG_TYPE = 0, 1, 2


# Test miner.api.create_game
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

    def testLose(self):
        """
        Should set board.lost to True after triggered boom.
        """
        board = Board(self.initial_field_data)
        board.mark()
        board.apply_action(CLICK, 1, 2)
        self.assertEqual(board.lost, True)

    def testShouldNotApplyActionAfterLose(self):
        board = Board(self.initial_field_data)
        board.mark()
        board.apply_action(CLICK, 1, 2)
        res = board.apply_action(CLICK, 0, 0)
        self.assertEqual(res, False)

    def testShouldNotApplyDoubleClickToEmptyCell(self):
        board = Board(self.initial_field_data)
        board.mark()
        res, _ = board.apply_action(DOUBLE_CLICK, 0, 0)
        self.assertEqual(res, False)

    def testShouldNotApplyDoubleClickWhenFlagCountNotMatch(self):
        board = Board(self.initial_field_data)
        board.mark()
        board.apply_action(CLICK, 0, 3)
        res, _ = board.apply_action(DOUBLE_CLICK, 0, 3)
        self.assertEqual(res, False)

    def testGivenInitialState(self):
        board = Board(self.initial_field_data, initial_state=self.initial_field_data)
        self.assertEqual(board.win, True)

    def testShouldNotAddFlag(self):
        """
        Should not add more flag than num_of_mines
        """
        board = Board(self.initial_field_data)
        board.mark()
        for (x, y) in [(0, 1), (0, 2), (0, 3)]:
            res, _ = board.apply_action(FLAG, x, y)
            self.assertEqual(res, True)
        res, _ = board.apply_action(FLAG, 4, 4)
        self.assertEqual(res, False)

    def testApplyActionToChangeStateEndToEnd(self):
        board = Board(self.initial_field_data)
        board.mark()
        board.apply_action(CLICK, 0, 3)
        self.assertEqual(
            board.state,
            [[None, None, None, 1, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]
        )
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
        res, new_state = board.apply_action(FLAG, 1, 2)
        self.assertEqual(res, True)
        self.assertEqual(new_state, board.state)
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
