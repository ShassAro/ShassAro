__author__ = 'roir'
from rest_framework import serializers

class GameUser():

    def __init__(self, name, password, vncPort):
        self.name = name
        self.password = password
        self.vncPort = vncPort



class GameUserSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()
    vncPort = serializers.IntegerField()

