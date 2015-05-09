from django.core import serializers
import json
import random
import requests
from rest_framework import status
from bl_exceptions import DeployError, DockerManagerNotAvailableError, DockerServerNotAvailableError
from models import Shassaro, GameUser, DockerManager, DockerServer


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
        which_symbol = random.choice('!@#')
        hash_list[symbol_pos] = which_symbol

    return "".join(hash_list)


def generate_initial_shassaro(participant, image):
    """
    Generate a Shassaro object
    :param participant: list of usernames that are to use this shassaro
    :param image: the image this shassaro will be using
    :return: the generated shassaro with goals hashes
    """
    shassaro = Shassaro()
    shassaro.docker_name = image.docker_name
    shassaro.save()

    game_user = GameUser()
    game_user.name = participant
    game_user.password = generate_password()
    game_user.save()
    shassaro.participants.add(game_user)

    shassaro.goals = [generate_goal() for goal in image.goal_description]
    shassaro.save()
    return shassaro


def generate_docker_server_dict():
    # Get all DockerServer objects into docker_servers_data list
    docker_servers = DockerServer.objects.all()
    if (len(docker_servers) == 0):
        raise DockerServerNotAvailableError()
    raw_docker_servers_data = serializers.serialize("python", docker_servers)
    docker_servers_data = [ds['fields'] for ds in raw_docker_servers_data]

    # Create a new docker_servers_list in which concatenate the protocol, ip and port for each docker server
    docker_servers_list = []
    for ds in docker_servers_data:
        docker_servers_list.append("{0}://{1}:{2}".format(ds['protocol'], ds['ip'], ds['port']))

    # add the 'docker_servers' key into the docker_servers_dict with the list as its value
    docker_servers_dict = {'docker_servers': docker_servers_list}

    # Go back
    return docker_servers_dict


def generate_shassaros_dict(shassaros):
    # Get shassaros into shassaros_data list
    raw_shassaros_data = serializers.serialize("python", shassaros)
    shassaros_data = [sh['fields'] for sh in raw_shassaros_data]

    for shassaro in shassaros_data:
        game_user = GameUser.objects.get(pk=shassaro['participants'][0])
        shassaro['participants'] = serializers.serialize("python", [game_user])[0]['fields']

    # Add the 'shassaros' key into the shassaros_dict
    shassaros_dict = {'shassaros': shassaros_data}

    # Go back
    return shassaros_dict


def generate_final_dict_to_send(docker_servers_dict, shassaros_dict):
    final_dict_to_send = {'dockerservers': docker_servers_dict['docker_servers'], 'shassaros': shassaros_dict['shassaros']}
    return final_dict_to_send


def deploy_shassaros(shassaros):
    """
    Sends a request to the Docker Manager to deploy 2 shassaros
    These shassaro objects represent a Game
    :param shassaros: List of exactly 2 Shassaro objects
    :return: The Shassaro objects populated with information from the Docker Manager
    """
    if shassaros is None or len(shassaros) != 2:
        raise ValueError("Number of passed ShassAro objects must be exactly 2")
    if not all(isinstance(x, Shassaro) for x in shassaros):
        raise TypeError("input must be of type {0}".format(Shassaro))

    managers = DockerManager.objects.all()
    if len(managers) == 0:
        raise DockerManagerNotAvailableError()
    docker_manager = managers[0]

    docker_manager_url = "http://{0}:{1}/".format(docker_manager.ip, docker_manager.port)
    if docker_manager.url != "/":
        docker_manager_url += "/{0}/".format(docker_manager.url)

    docker_manager_url += "deploy"

    docker_servers_dict = generate_docker_server_dict()
    shassaros_dict = generate_shassaros_dict(shassaros)

    try:
        # make the request
        response = requests.post(docker_manager_url,
                                 json=generate_final_dict_to_send(docker_servers_dict, shassaros_dict))
    except Exception as e:
        raise DeployError("Error sending a request to the docker manager", e)

    # validate response status code
    if response.status_code != status.HTTP_200_OK:
        raise DeployError("status_code:{0} response:{1}".format(response.status_code, response.text))

    # parse the response & populate the shassaro objects
    try:
        shassaros_json = response.json()
        for i in range(shassaros.count()):
            shassaros[i].shassaro_ip = shassaros_json["shassaros"][i]["shassaro_ip"]
            shassaros[i].docker_server_ip = shassaros_json["shassaros"][i]["docker_server_ip"]
            shassaros[i].docker_id = shassaros_json["shassaros"][i]["docker_id"]

            # Getting the vncport. using the first, because we currently suport only one user
            user_temp_obj = shassaros[i].participants.first()
            user_temp_obj.vnc_port = int(shassaros_json["shassaros"][i]["participants"]["vnc_port"])
            user_temp_obj.save()

            shassaros[i].save()

        return shassaros

    except Exception as e:
        raise DeployError(e.message)