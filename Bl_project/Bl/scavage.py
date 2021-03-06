from end_game import end_game
from models import Game, Shassaro, DockerManager, DockerServer
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta, datetime
import requests
import json
import logging

logger = logging.getLogger(__name__)

def scavage_games():
    try:
        games = Game.objects.all()

        # Scavage over-time games
        for game in games:
            delete_game_bool = False
            if game.start_time is None:
                delete_game_bool = True
            else:
                max_time = (game.start_time + timedelta(0, game.duration_minutes * 60)).replace(tzinfo=None)
                now_time = datetime.now().replace(tzinfo=None)
                if max_time < now_time:
                    delete_game_bool = True

            if delete_game_bool:
                if (game.userA is None) or (game.userA == '') or (game.userB == '') or (game.userB is None):
                    game.delete()
                else:
                    end_game(game, [], [game.userA, game.userB], True)

                return "Games running in over-time found and dealt with"

        return "OK"

    except Exception as e:
        return "Something went wrong. Exception: " + str(e) + str(e.message)


def scavage_defunct_shassaros():
    try:
        shassaros = Shassaro.objects.all()
        found_defunct = False

        # Scavage defunct shassaros
        for shassaro in shassaros:
            if (shassaro.docker_id is None) or (shassaro.docker_server_ip is None) or (shassaro.shassaro_ip is None):
                shassaro.delete()
                found_defunct = True

        if found_defunct:
            return "Shassaros with defunct data found and dealt with"
        else:
            return "OK"

    except Exception as e:
        return "Something went wrong. Exception: " + str(e) + str(e.message)


def scavage_orphand_dockers():
    try:
        logger.debug("Started scavage_orphand_docker()")

        str_to_return = ''

        # Scavage dockers that are running with no active game
        valid_docker_ids = []
        games = Game.objects.all()
        for game in games:
            for shassaro in game.shassaros.all():
                valid_docker_ids.append(shassaro.docker_id)

        # Get Docker Manager List URL
        docker_manager_obj = DockerManager.objects.all()[0]
        docker_manager_url = "http://{0}:{1}/api/docker/list".format(docker_manager_obj.ip, docker_manager_obj.port)

        logger.debug("Docker manager URL: {0}".format(docker_manager_url))

        json_to_send = {"dockerServers": []}

        # Get Docker Servers
        docker_servers_obj = DockerServer.objects.all()
        for docker_server_obj in docker_servers_obj:
            json_to_send['dockerServers'].append("{0}://{1}:{2}"
                .format(docker_server_obj.protocol, docker_server_obj.ip, docker_server_obj.port))

        logger.debug("Sending {0} json to server.".format(json_to_send))

        # Send a list get request to the Docker Manager
        response = requests.get(docker_manager_url, json=json_to_send)

        logger.debug("Got response: {0} from server.".format(response))

        if response.status_code != status.HTTP_200_OK:
            str_to_return = "An error has occurred while getting the docker list"

        docker_servers_and_ids = json.loads(response.content)

        #logger.debug("Docker servers and ids: {0}".foramt(docker_servers_and_ids))

        # Remove valid docker ids from the list
        for docker_id in valid_docker_ids:
            for docker_server in docker_servers_and_ids:
                if docker_id in docker_servers_and_ids[docker_server]:
                    docker_servers_and_ids[docker_server].remove(docker_id)

        # Remove docker servers with no remaining docker ids from the dict
        for docker_server in docker_servers_and_ids:
            if len(docker_server) == 0:
                docker_servers_and_ids.remove(docker_server)

        # If orphan docker ids found
        if len(docker_servers_and_ids) > 0:
            #logger.debug("Found docker server with orphan dockers: {0}".format(docker_servers_and_ids))
            dockers_running_with_no_game_bool = True
            str_to_return = "Found dockers running with no game"

            # Kill bastard dockers
            for docker_server in docker_servers_and_ids:
                for docker_id in docker_servers_and_ids[docker_server]:
                    kill_json = {
                        "dockerServerIp": docker_server,
                        "dockerId": [
                                docker_id,
                                ''
                        ]
                    }

                    # Get Docker Manager Kill URL
                    docker_manager_obj = DockerManager.objects.all()[0]
                    docker_manager_url = "http://{0}:{1}/api/docker/kill".format(docker_manager_obj.ip, docker_manager_obj.port)

                    logger.debug("Docker Manager Kill URL: {0}".format(docker_manager_url))

                    # Send the kill!
                    response = requests.post(docker_manager_url, json=kill_json)

                    logger.debug("Got response: {0} from server.".format(response))

                    if response.status_code != status.HTTP_200_OK:
                        pass
                    else:
                        str_to_return = "Found dockers running with no game and dealt with them"

        # Nothing wrong happened :)
        if str_to_return == '':
            return 'OK'
        else:
            return str_to_return

    except Exception as e:
        return "Something went wrong. Exception: " + str(e)

def scavage():
    logger.debug("scavage() --- started")

    # Init objects
    statuses = {}

    # Init booleans
    dockers_running_with_no_game_bool = False

    statuses['games'] = scavage_games()
    logger.debug("scavage() --- got scavage_games() result: {0}".format(statuses['games']))

    statuses['defunct_shassaro'] = scavage_defunct_shassaros()
    logger.debug("scavage() --- got scavage_defunct_shassaros() result: {0}"
                 .format(statuses['defunct_shassaro']))

    statuses['dockers_running_with_no_game'] = scavage_orphand_dockers()
    logger.debug("scavage() --- got dockers_running_with_no_game() result: {0}"
                 .format(statuses['dockers_running_with_no_game']))

    # Return scavaging results
    all_ok_bool = True
    for key in statuses.keys():
        if statuses[key] is not "OK":
            all_ok_bool = False

    if all_ok_bool:
        statuses_json = '{"statuses": {"all":"OK"}}'
    else:
        statuses_json = '{"statuses":' + str(statuses) + '}'

    return Response(data=statuses_json, status=status.HTTP_200_OK)

