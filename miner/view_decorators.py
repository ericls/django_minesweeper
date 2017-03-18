import json
from django.http import JsonResponse
from miner.models import Game


def require_post_and_json(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.method == 'POST':
            return JsonResponse(status=405, data={"error": "Method not allowed. Please use POST to create game"})
        if not request.content_type == 'application/json':
            return JsonResponse(status=415, data={"error": "I need json"})
        try:
            post_data = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(status=400, data={"error": "Invalid input json"})
        request.json = post_data
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def with_game(view_func):
    def _wrapped_view_func(request, pk, *args, **kwargs):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return JsonResponse(
                status=404, data={"error": "Unable to find game"}
            )
        request.game = game
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
