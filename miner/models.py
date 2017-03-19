import json
import copy
from django.db import models
from miner.Board import Board, CLICK, DOUBLE_CLICK, FLAG


class Game(models.Model):
    """
    Game model.
    This model only stores the initial board of the game.
    """

    board = models.TextField()

    def apply_action(self, action_type, x, y):
        """
        Add an action to the game.
        The action is persisted in database only when it has effect on the state.
        :param action_type: CLICK | DOUBLE_CLICK | FLAG
        :param x: coordinate X
        :param y: coordinate Y
        :return: None
        """
        board = self._current_board
        current_state = copy.deepcopy(board.state)
        board.apply_action(action_type, x, y)
        if not board.state == current_state:
            GameAction.objects.create(game_id=self.id, action_type=action_type, x=x, y=y)
        return

    def go_back(self):
        """
        Remove the latest applied action from the game.
        :return: None
        """
        last_action = self.actions.order_by('id').last()
        if last_action:
            last_action.delete()

    @property
    def latest_state(self):
        """
        :return: the latest state of the game.
        """
        board = self._current_board
        return {
            "state": board.state,
            "win": board.win,
            "lost": board.lost,
            "minesLeft": board.mines_left,
        }

    @property
    def _current_board(self):
        """
        :return: A Board instance representing the current game with all saved actions applied.
        """
        actions = self.actions.order_by('id').all()
        board = Board(json.loads(self.board))
        for action in actions:
            board.apply_action(action.action_type, action.x, action.y)
        return board


class GameAction(models.Model):

    ACTION_TYPES = (
        (CLICK, "CLICK"),
        (DOUBLE_CLICK, "DOUBLE_CLICK"),
        (FLAG, "FLAG")
    )

    game = models.ForeignKey(Game, related_name="actions")
    x = models.IntegerField()
    y = models.IntegerField()
    action_type = models.IntegerField(choices=ACTION_TYPES)
