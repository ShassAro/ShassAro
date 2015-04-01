import random
import requests
from rest_framework import status
from exceptions import DeployFailedException
from models import Shassaro, GameUser


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


def deploy_shassaros(shassaros):
    if shassaros.count() != 2:
        raise ValueError("Number of passed ShassAro objects must be exactly 2")

    # make the request
    url = "http://dockerserver/dockers/deploy"
    response = requests.post(url, data=shassaros)

    # validate response status code
    if response.status_code != status.HTTP_200_OK:
        raise DeployFailedException("status_code:{0} response:{1}".format(response.status_code, response.text))

    # parse the response & populate the shassaro objects
    try:
        shassaros_json = response.json()
        for i in range(shassaros.count()):
            shassaros[i].shassaro_ip = shassaros_json[i].shassaro_ip
            shassaros[i].docker_server_ip = shassaros_json[i].docker_server_ip
            shassaros[i].docker_id = shassaros_json[i].docker_id

        return shassaros

    except Exception as e:
        raise DeployFailedException(e.message)