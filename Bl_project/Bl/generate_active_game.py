from django.db.models import Q
from models import *


def GenerateActiveGame(username):

    user_index = 0
    # Get the game object. Try userA first.
    gameObj = Game.objects.filter(userA=username)

    if (len(gameObj) == 0):

        # Lets try userB
        gameObj = Game.objects.filter(userB=username)
        user_index = 1

    # If none found -> game is over. return gameresult.
    if (len(gameObj) == 0):

        # Find all game result that the user is a member of
        allGames = GameResult.objects.filter(Q(losing_users__username=username) | Q(winning_users__username=username))

        # Redirect to gameresult to the last game of all
        return "/game_results/{0}".format(allGames.order_by("-start_time")[0].pk)

    # Assume two user have different images
    image_index = user_index

    # Find out if the users uses the same image
    if (len(gameObj[0].images.all()) == 1):
        image_index = 0 # Force the usage of the first image

    returnJson = {
        "username" : gameObj[0].shassaros.all()[user_index].participants.all()[0].name,
        "vnc_port" : gameObj[0].shassaros.all()[user_index].participants.all()[0].vnc_port,
        "password" : gameObj[0].shassaros.all()[user_index].participants.all()[0].password,
        "goals" : gameObj[0].images.all()[image_index].goal_description,
        "hints" : gameObj[0].images.all()[image_index].hints,
        "duration" : gameObj[0].images.all()[image_index].duration_minutes,
        "start_time" :str(gameObj[0].start_time),
        "remote_ip" : gameObj[0].shassaros.all()[abs(user_index-1)].shassaro_ip,
        "docker_manager_ip": DockerManager.objects.first().ip,
        "remote_username" : gameObj[0].shassaros.all()[abs(user_index-1)].participants.all()[0].name,
        "remote_email" : User.objects.filter(username=gameObj[0].shassaros
                                             .all()[abs(user_index-1)].participants.all()[0].name).first().email,
        "remote_goals_count" : 0 if gameObj[0].shassaros.all()[user_index].goals_completed == None
                                        else len(gameObj[0].shassaros.all()[user_index].goals_completed)
    }

    return returnJson
