__author__ = 'roir'
from rest_framework import serializers
from GameUser import GameUserSerializer

class ShassAro():

    def __init__(self, goals, participants, shassaro_ip, docker_server_ip, docker_id):
        self.goals = goals
        self.participants = participants
        self.shassaroIp = shassaro_ip
        self.dockerServerIp = docker_server_ip
        self.dockerId = docker_id


class ShassaroSerializer(serializers.Serializer):
        goals = serializers.ListField()
        participants = GameUserSerializer(many=True)
        shassaroIp = serializers.CharField()
        dockerServerIp = serializers.CharField()
        dockerId = serializers.CharField()

