__author__ = 'roir'
from rest_framework import serializers

class GameUser():

    def __init__(self, name, password, vnc_port):
        self.name = name
        self.password = password
        self.vnc_port = vnc_port



class GameUserSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()
    vnc_port = serializers.IntegerField()

