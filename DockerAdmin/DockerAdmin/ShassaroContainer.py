from ShassAro import ShassaroSerializer

__author__ = 'roir'
from rest_framework import serializers

class ShassaroContainer():

    def __init__(self, shassros):
        self.shassaros = shassros



class ShassaroContainerSerializer(serializers.Serializer):
    shassaros = ShassaroSerializer(many=True)
