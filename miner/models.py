import json
from django.db import models

GameActionTypes = [
    "CLICK",
    "FLAG"
]

CELL_STATES = [
    "SHOWN",
    "HIDDEN",
    "FLAGGED"
]


class Game(models.Model):

    board = models.TextField()


class GameActions(models.Model):

    ACTION_TYPES = map(
        lambda i: (i, GameActionTypes[i]),
        range(len(GameActionTypes))
    )

    game = models.ForeignKey(Game)
    x = models.IntegerField()
    y = models.IntegerField()
    action_type = models.IntegerField(choices=ACTION_TYPES)
