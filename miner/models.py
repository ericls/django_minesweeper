import json
from django.db import models
from miner.utils import Board, GameActionTypes


class Game(models.Model):

    board = models.TextField()

    def back(self):
        last_action = self.actions.order_by('id').last()
        if last_action:
            last_action.delete()

    @property
    def latest_state(self):
        actions = self.actions.order_by('id').all()
        board = Board(json.loads(self.board))
        for action in actions:
            board.apply_action(GameActionTypes[action.action_type], action.x, action.y)
        return board.state


class GameAction(models.Model):

    ACTION_TYPES = map(
        lambda i: (i, GameActionTypes[i]),
        range(len(GameActionTypes))
    )

    game = models.ForeignKey(Game, related_name="actions")
    x = models.IntegerField()
    y = models.IntegerField()
    action_type = models.IntegerField(choices=ACTION_TYPES)
