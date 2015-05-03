__author__ = 'roir'
from rest_framework import serializers
from GameUser import GameUserSerializer

class ShassAro():

    def __init__(self, goals, participants, shassaro_ip, docker_server_ip, docker_id, docker_name):
        self.goals = goals
        self.participants = participants
        self.shassaro_ip = shassaro_ip
        self.docker_server_ip = docker_server_ip
        self.docker_id = docker_id
        self.docker_name = docker_name


class ShassaroSerializer(serializers.Serializer):
        goals = serializers.ListField()
        participants = GameUserSerializer(many=True)
        shassaro_ip = serializers.CharField()
        docker_server_ip = serializers.CharField()
        docker_id = serializers.CharField()
        docker_name = serializers.CharField()

