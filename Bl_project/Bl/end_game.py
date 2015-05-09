from datetime import *
from django.contrib.auth.models import User
import requests
from rest_framework import status
from bl_exceptions import DockerManagerNotAvailableError, KillError
from models import DockerManager, GameResult, GameRequest


def end_game(game_obj, username_winner, username_loser):

    # Create the kill command json
    kill_json =  {
            "dockerServerIp": game_obj.shassaros.first().docker_server_ip,
            "dockerId": [
                game_obj.shassaros.all()[0].docker_id,
                game_obj.shassaros.all()[1].docker_id
            ]
        }

    # Get the docker manager
    managers = DockerManager.objects.all()
    if len(managers) == 0:
        raise DockerManagerNotAvailableError()
    docker_manager = managers[0]

    # Is there a postfix?
    docker_manager_url = "http://{0}:{1}/".format(docker_manager.ip, docker_manager.port)
    if docker_manager.url != "/":
        docker_manager_url += "/{0}/".format(docker_manager.url)

    # Append the command name
    docker_manager_url += "kill"

    # Send the kill!
  #  response = requests.post(docker_manager_url, json=kill_json)

   # if response.status_code != status.HTTP_200_OK:
   #     raise KillError("status_code:{0} response:{1}".format(response.status_code, response.text))

    # Lets create a game result!
    game_result = GameResult()

    # Is computer?
    game_result.computer = game_obj.computer

    # Calculate the duration, in minutes
    game_result.actual_duration_minutes = \
        (datetime.now().replace(tzinfo=None) - game_obj.start_time.replace(tzinfo=None)).seconds / 60

    # Set the start time
    game_result.start_time = game_obj.start_time

    # Set the experience gained from this challenge
    game_result.experience_gained = calculate_exprience_gained()

    # Saving before establishing any many-to-many relationships
    game_result.save()

    # Set the winning and losing users
    game_result.losing_users.add(User.objects.filter(username=username_loser)[0])
    game_result.winning_users.add(User.objects.filter(username=username_winner)[0])

    # Add the tags, from each image
    for image in game_obj.images.all():
        for tag in image.tags.all():
            game_result.tags.add(tag)

    # Save!
    game_result.save()

    # Now lets clean up..
    for shassaro in game_obj.shassaros.all():
        for gameuser in shassaro.participants.all():
            gameuser.delete()
        shassaro.delete()

    for game_request in GameRequest.objects.filter(game=game_obj):
        game_request.delete()

    game_obj.delete()


def calculate_exprience_gained():
    #TODO: something smarter..
    return 100