from end_game import end_game
from models import Game
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta, datetime

def scavage():
    # Get all games
        games = Game.objects.all()

        for game in games:
            max_time = (game.start_time + timedelta(0, game.duration_minutes * 60)).replace(tzinfo=None)
            now_time = datetime.now().replace(tzinfo=None)
            if (max_time < now_time):
                end_game(game, [], [game.userA, game.userB], True)
                return Response('{"status": "Games running in over-time found and dealt with."}', status=status.HTTP_200_OK)

        return Response('{"status": "Nothing to scavage."}', status=status.HTTP_200_OK)
