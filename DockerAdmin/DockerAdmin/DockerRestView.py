from xml.sax import default_parser_list

__author__ = 'roir'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from DockerManager import DockerDeploy, DockerKill, DockerScavage
from ShassAro import ShassAro, ShassaroSerializer
from Exceptions import *
from ShassaroContainer import ShassaroContainerSerializer


class DockerDeployRestView(APIView):

    def post(self, request, *args, **kw):

        # The raw shassaros as accepted from REST
        rawShssaros = []

        # Placeholder for the instances
        shassaroInstances = []

        try:
            # Get the two shassaros
            rawShssaros.append(request.DATA['shassaros'][0])
            rawShssaros.append(request.DATA['shassaros'][1])

            for currShassaro in rawShssaros:

                # Get the parameters from the post request
                goals = currShassaro['goals']
                participants = currShassaro['participants']
                shassaro_ip = currShassaro['shassaroIp']
                docker_server_ip = currShassaro['dockerServerIp']
                docker_id = currShassaro['dockerId']

                # Create a shassaro instance from them
                inst = ShassAro(goals, participants, shassaro_ip, docker_server_ip, docker_id)

                # Add it to the list
                shassaroInstances.append(inst)

        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        # Pass it to Dockermanager
        deployClass = DockerDeploy(shassaroInstances, *args, **kw)

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

            dockerId = []

            # Get the two shassaros
            dockerServerIp = request.DATA['dockerServerIp']
            dockerId.append(request.DATA['dockerId'][0])
            dockerId.append(request.DATA['dockerId'][1])


        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        # Pass it to Dockermanager
        killClass = DockerKill(dockerServerIp, dockerId, *args, **kw)

        # Just declare it out of scope
        response=""

        try:
            # Get the result
            result = killClass.kill()

            response = Response("", status=status.HTTP_200_OK)

        except ShassAroException as e:

            response = Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return response



