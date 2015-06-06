from xml.sax import default_parser_list

__author__ = 'roir'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from DockerManager import DockerDeploy, DockerKill, DockerScavage
from ShassAro import ShassAro, ShassaroSerializer
from Exceptions import *
from ShassaroContainer import ShassaroContainerSerializer
from docker import Client

class DockerDeployRestView(APIView):

    def post(self, request, *args, **kw):

        # The raw shassaros as accepted from REST
        rawShssaros = []

        # Placeholder for the instances
        shassaroInstances = []

        # Placeholder for docker servers
        dockerServers = []

        try:
            # Get the two shassaros
            rawShssaros.append(request.DATA['shassaros'][0])
            rawShssaros.append(request.DATA['shassaros'][1])

            for currShassaro in rawShssaros:

                # Get the parameters from the post request
                goals = currShassaro['goals']
                participants = currShassaro['participants']
                shassaro_ip = currShassaro['shassaro_ip']
                docker_server_ip = currShassaro['docker_server_ip']
                docker_id = currShassaro['docker_id']
                docker_name = currShassaro['docker_name']

                # Create a shassaro instance from them
                inst = ShassAro(goals, participants, shassaro_ip, docker_server_ip, docker_id, docker_name)

                # Add it to the list
                shassaroInstances.append(inst)

            dockerServers = (request.DATA['dockerservers'])

        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        # Pass it to Dockermanager
        deployClass = DockerDeploy(shassaroInstances, dockerServers, *args, **kw)

        # Just declare it out of scope
        response=""

        try:
            # Get the result
            result = deployClass.deploy()

            shaContainer = ShassaroContainerSerializer(result)

            response = Response(shaContainer.data, status=status.HTTP_200_OK)

        except ShassAroException as e:

            response = Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

class DockerKillRestView(APIView):

    def post(self, request, *args, **kw):

        try:
            # Get the two shassaros
            dockerServerIp = request.DATA['dockerServerIp']
            dockerId1 = request.DATA['dockerId'][0]
            dockerId2 = request.DATA['dockerId'][1]


        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        # Pass it to Dockermanager
        killClass1 = DockerKill(dockerServerIp, dockerId1, *args, **kw)
        killClass2 = DockerKill(dockerServerIp, dockerId2, *args, **kw)

        # Just declare it out of scope
        response=""

        try:
            # Get the result
            killClass1.kill()
            killClass2.kill()

            response = Response("", status=status.HTTP_200_OK)

        except ShassAroException as e:

            response = Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return response


class DockerListRestView(APIView):

    def get(self, request, *args, **kw):

        try:
            # Get the two shassaros
            dockerServers = request.DATA['dockerServers']

        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        docker_ids = {}

        try:

            for dockerServer in dockerServers:
                docker_client = Client(base_url=dockerServer)
                containers = docker_client.containers()
                if len(containers) > 0:
                    docker_ids[dockerServer] = []
                    for container in containers:
                        docker_ids[dockerServer].append(container['Id'])
        except Exception as e:
            return Response(data=str(e.message), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=docker_ids, status=status.HTTP_200_OK)