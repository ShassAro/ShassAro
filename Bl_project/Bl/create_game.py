from django.core import serializers
import random
import requests
from rest_framework import status
from bl_exceptions import DeployError, DockerManagerNotAvailableError
from models import Shassaro, GameUser, DockerManager


__author__ = 'shay'


def generate_goal():
    """
    Generates a random hash (128 bits)
    :return: Hex value of the hash
    """
    hash_string = random.getrandbits(128)
    return '%032x' % hash_string


def generate_password():
    """
    Generates a random hash (32 bits)
    :return: Hex value of the hash
    """
    hash_string = random.getrandbits(32)  # Generate a random bit string of 32 bits
    hash_list = list('%008x' % hash_string)  # hex those random bits into a list

    # Switch 1/2 of the hex chars into special symbols
    for x in xrange(2):
        symbol_pos = random.randint(0, 7)
        which_symbol = random.choice('~!@#$%^&*()_+')
        hash_list[symbol_pos] = which_symbol

    return "".join(hash_list)


def generate_initial_shassaro(participants, image):
    """
    Generate a Shassaro object
    :param participants: list of usernames that are to use this shassaro
    :param image: the image this shassaro will be using
    :return: the generated shassaro with goals hashes
    """
    shassaro = Shassaro()
    for participant in participants:
        game_user = GameUser()
        game_user.name = participant
        game_user.password = generate_password()
        shassaro.participants.add(game_user)

    shassaro.goals = [generate_goal() for goal in image.goal_description]
    return shassaro

# def mock_2_shassaros():



def deploy_shassaros(shassaros):
    if shassaros is None or len(shassaros) != 2:
        raise ValueError("Number of passed ShassAro objects must be exactly 2")
    if not all(isinstance(x, Shassaro) for x in shassaros):
        raise TypeError("input must be of type {0}".format(Shassaro))

    managers = DockerManager.objects.all()
    if len(managers) == 0:
        raise DockerManagerNotAvailableError()
    docker_manager = managers[0]
    docker_manager_url = "http://{0}:{1}/deploy".format(docker_manager.ip, docker_manager.port)

    try:
        # make the request
        response = requests.post(docker_manager_url, data=serializers.serialize("json", shassaros))
    except Exception as e:
        raise DeployError("Error sending a request to the docker manager", e)

    # validate response status code
    if response.status_code != status.HTTP_200_OK:
        raise DeployError("status_code:{0} response:{1}".format(response.status_code, response.text))

    # parse the response & populate the shassaro objects
    try:
        shassaros_json = response.json()
        for i in range(shassaros.count()):
            shassaros[i].shassaro_ip = shassaros_json[i].shassaro_ip
            shassaros[i].docker_server_ip = shassaros_json[i].docker_server_ip
            shassaros[i].docker_id = shassaros_json[i].docker_id

        return shassaros

    except Exception as e:
        raise DeployError(e.message)