from rest_framework import serializers
from models import *

__author__ = 'assaf'


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'description')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('pk', 'docker_name', 'description', 'tags', 'level', 'allow_in_game', 'hints',
                  'goal_description', 'post_script_name', 'duration_minutes')


class LearningPathSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LearningPath
        fields = ('pk', 'subject', 'images', 'color', 'description')


class GameUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameUser
        fields = ('pk', 'name', 'password', 'vnc_port')


class ShassaroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shassaro
        fields = ('pk', 'goals', 'participants', 'shassaro_ip', 'docker_server_ip', 'docker_id')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('pk', 'group1', 'group2', 'computer', 'images', 'shassaros', 'start_time', 'goals_completed',
                  'duration_minutes')


class GameResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameResult
        fields = ('pk', 'losing_users', 'winning_users', 'computer', 'start_time', 'actual_duration_minutes', 'tags',
                  'experience_gained')


class BadgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Badge
        fields = ('name', 'class_name', 'experience')


class DockerManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DockerManager
        fields = ('pk', 'name', 'ip', 'port', 'url')


class DockerServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DockerServer
        fields = ('pk', 'name', 'protocol', 'ip', 'port')


class ConfigurationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Configurations
        fields = ('pk', 'docker_server')