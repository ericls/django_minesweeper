import json
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from miner.models import Game
from miner.Board import Board

logger = logging.getLogger(__name__)


def create_game(request):
    if not request.method == 'POST':
        return JsonResponse(status=405, data={"error": "Method not allowed. Please use POST to create game"})
    if not request.content_type == 'application/json':
        return JsonResponse(status=415, data={"error": "I need json"})
    try:
        post_data = json.loads(request.body.decode('utf-8'))
        num_of_mines, size = post_data["numOfMines"], post_data["size"]
    except Exception as e:
        logger.exception(e)
        return JsonResponse(
            status=400,
            data={"error": "invalid input json"}
        )
    try:
        board = Board.generate_new_board(size, num_of_mines).board
        game = Game.objects.create(board=board)
    except Exception as e:
        logger.exception(e)
        return JsonResponse(
            status=500,
            data={"error", "Failed to create game"}
        )
    return JsonResponse(
        status=201,
        data={"gameId": game.id}
    )

