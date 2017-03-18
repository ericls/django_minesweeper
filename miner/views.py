from django.shortcuts import render
from miner.view_decorators import with_game


def index(request):
    return render(request, 'miner/index.html')


@with_game
def show_game(request):
    return render(request, 'miner/index.html', {"initialGameId": request.game.id})
