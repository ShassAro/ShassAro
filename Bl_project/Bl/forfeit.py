from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from models import Game
from end_game import end_game


def forfeit(username):

    # Get user object
    user_obj = User.objects.filter(username=username)

    # User does not exist on the DB
    if len(user_obj) == 0:
        return Response(data="Username does not exist", status=status.HTTP_400_BAD_REQUEST)

    # Get user's Game object

    game_obj = Game.objects.filter(userA=username).order_by("-start_time")
    user_index = 0

    # Try userB
    if len(game_obj) == 0:
        game_obj = Game.objects.filter(userB=username).order_by("-start_time")
        user_index = 1

    # No games found for user
    if len(game_obj) == 0:
        return Response(data="User does not have an active game", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Get other username
    if user_index == 0:
        other_username = game_obj[0].userB
    else:
        other_username = game_obj[0].userA

    # End the game
    try:
        end_game(game_obj[0], other_username, username)
        return Response(data="game ended", status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)