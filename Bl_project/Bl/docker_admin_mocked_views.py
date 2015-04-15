from Bl.serializers import ShassaroSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView


@api_view(['GET'])
def deploy(request):
    if request.method == 'GET':
        if request.data is None:
            return Response("Empty input", status=HTTP_400_BAD_REQUEST)
        serializer = ShassaroSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response("Invalid input",status=HTTP_400_BAD_REQUEST)

        shassaros = serializer.data
        for shassaro in shassaros:
            shassaro.shassaro_ip = "192.168.1.13"
            shassaro.docker_server_ip = "192.168.2.1"
            shassaro.docker_id = 1

        return Response(data=shassaros, status=HTTP_200_OK)