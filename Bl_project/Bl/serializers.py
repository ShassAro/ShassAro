from rest_framework import serializers
from models import *


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'description')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('docker_name', 'description', 'tags', 'level', 'allow_in_game', 'hints',
                  'goal_description', 'post_script_name', 'duration_minutes')


class LearningPathSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LearningPath
        fields = ('pk', 'subject', 'images', 'color', 'description')


class GameRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameRequest
        fields = ('username', 'tags', 'submitted_at', 'status', 'game')

class GameRequestStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameRequestStatus
        fields = ('status', 'message')

class GameUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameUser
        fields = ('pk', 'name', 'password', 'vnc_port')


class ShassaroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shassaro
        fields = ('pk', 'goals', 'participants', 'shassaro_ip', 'docker_server_ip', 'docker_id', 'docker_name',
                  'goals_completed')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class GameSerializer(serializers.HyperlinkedModelSerializer):

    images = ImageSerializer(many=True)

    class Meta:
        model = Game
        fields = ('pk', 'userA', 'userB', 'computer', 'images', 'shassaros', 'start_time',
                  'duration_minutes')


class GameResultSerializer(serializers.HyperlinkedModelSerializer):

    losing_users = UserSerializer(many=True)
    winning_users = UserSerializer(many=True)

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