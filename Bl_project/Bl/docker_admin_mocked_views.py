from serializers import ShassaroSerializer
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import *


@api_view(['POST'])
def deploy(request):
    if request.method == 'POST':
        shassaros = serializers.deserialize("json", request.data)

        # serializer = ShassaroSerializer(data=request.data["shassaros"], many=True, context={'request': request})
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        #
        # shassaros = serializer.data
        if len(shassaros) != 2:
            return Response("Must provide exactly 2 shassaro objects", status=HTTP_400_BAD_REQUEST)
        for shassaro in shassaros:
            shassaro.shassaro_ip = "192.168.1.13"
            shassaro.docker_server_ip = "192.168.2.1"
            shassaro.docker_id = 1

        return Response(data=shassaros, status=HTTP_200_OK)