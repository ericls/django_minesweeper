import json
from django.db import models
from miner.Board import Board, CLICK, DOUBLE_CLICK, FLAG


class Game(models.Model):

    board = models.TextField()

    # TODO: ensure board is marked

    def apply_action(self, action_type, x, y):
        # TODO: Check if the action can be applied
        GameAction.objects.create(game_id=self.id, action_type=action_type, x=x, y=y)

    def go_back(self):
        last_action = self.actions.order_by('id').last()
        if last_action:
            last_action.delete()

    @property
    def latest_state(self):
        actions = self.actions.order_by('id').all()
        board = Board(json.loads(self.board))
        for action in actions:
            board.apply_action(action.action_type, action.x, action.y)
        return {
            "state": board.state,
            "win": board.win,
            "lost": board.lost,
            "boomed": board.boomed,
            "minesLeft": board.mines_left,
        }


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
