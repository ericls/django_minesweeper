import logging
from django.shortcuts import render
from django.http import JsonResponse
from miner.models import Game
from miner.Board import Board
from miner.view_decorators import require_post_and_json, with_game

logger = logging.getLogger(__name__)


@require_post_and_json
def create_game(request):
    try:
        num_of_mines, size = request.json["numOfMines"], request.json["size"]
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


@with_game
def get_game(request):
    return JsonResponse(
        status=200,
        data=request.game.latest_state
    )


@require_post_and_json
@with_game
def apply_action(request):
    try:
        action_type, x, y = request.json["action_type"], request.json["x"], request.json["y"]
    except Exception as e:
        logger.exception(e)
        return JsonResponse(
            status=400,
            data={"error": "invalid input json"}
        )
    request.game.apply_action(action_type, x, y)
    return JsonResponse(
        status=200,
        data=request.game.latest_state
    )


@with_game
def go_back(request):
    request.game.go_back()
    return JsonResponse(
        status=200,
        data=request.game.latest_state
    )
