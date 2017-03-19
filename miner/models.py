import json
import logging
from django.db import models, transaction, IntegrityError
from miner.Board import Board, CLICK, DOUBLE_CLICK, FLAG

logger = logging.getLogger(__name__)


class Game(models.Model):
    """
    Game model.
    This model persists the initial board and current state of a game.
    """

    board = models.TextField()
    state = models.TextField(blank=True, null=True)

    def apply_action(self, action_type, x, y):
        """
        Add an action to the game.
        The action is persisted in database only when it has effect on the state.
        :param action_type: CLICK | DOUBLE_CLICK | FLAG
        :param x: coordinate X
        :param y: coordinate Y
        :return: updated game instance
        """
        board = self._current_board
        valid, new_state = board.apply_action(action_type, x, y)
        if valid:
            try:
                with transaction.atomic():
                    GameAction.objects.create(game_id=self.id, action_type=action_type, x=x, y=y)
                    self.state = json.dumps(new_state)
                    self.save()
            except IntegrityError as e:
                logger.exception(e)
        return self

    def go_back(self):
        """
        Remove the latest applied action from the game.
        :return: updated game instance. If transaction failed, return the current instance
        """
        last_action = self.actions.order_by('id').last()
        if last_action:
            try:
                with transaction.atomic():
                    last_action.delete()
                    return self.sync_state()
            except IntegrityError as e:
                logger.exception(e)
                return self

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

    def sync_state(self):
        """
        Synchronize state by applying all saved actions to the initial board in order
        :return: Updated game instance
        """
        board = Board(json.loads(self.board))
        for action in self.actions.all().order_by('id'):
            board.apply_action(action.action_type, action.x, action.y)
        self.state = json.dumps(board.state)
        self.save()
        return self

    @property
    def _current_board(self):
        """
        :return: A Board instance representing the current game with all saved actions applied.
        """
        if not self.state:
            initial_state = None
        else:
            initial_state = json.loads(self.state)
        board = Board(json.loads(self.board), initial_state=initial_state)
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
