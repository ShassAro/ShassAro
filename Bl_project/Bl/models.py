from django.contrib.auth.models import User
from jsonfield import JSONField
from django.db import models

__author__ = 'shay'

# TODO: Bring back the primary_key=True to the necessary fields. Shay removed them because they were causing issues with duplicated fields.


class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()


class Image(models.Model):
    docker_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    level = models.PositiveIntegerField()
    allow_in_game = models.BooleanField(default=False)
    hints = JSONField()  # represented as a json array
    goal_description = JSONField()  # JSON describing the goals in this image
    post_script_name = models.TextField()  # String to represent either script name, or script path
    duration_minutes = models.PositiveIntegerField()


class LearningPath(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    images = models.ManyToManyField(Image)
    # picture = models.ImageField()
    color = models.CharField(max_length=100)
    description = models.TextField()


class GameUser(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    vnc_port = models.PositiveIntegerField()


class Shassaro(models.Model):
    goals = JSONField()  # JSON-serialized (text) version of the goals
    participants = models.ManyToManyField(GameUser)
    shassaro_ip = models.GenericIPAddressField()
    docker_server_ip = models.GenericIPAddressField()
    docker_id = models.CharField(max_length=100)


class Game(models.Model):
    group1 = models.ManyToManyField(User, related_name='group1')
    group2 = models.ManyToManyField(User, related_name='group2')
    computer = models.BooleanField(default=False)
    images = models.ManyToManyField(Image)
    shassaros = models.ManyToManyField(Shassaro)
    start_time = models.DateTimeField()
    goals_completed = JSONField()
    duration_minutes = models.PositiveIntegerField()


class GameResult(models.Model):
    losing_users = models.ManyToManyField(User, related_name='losing_users')
    winning_users = models.ManyToManyField(User, related_name='winning_users')
    computer = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    actual_duration_minutes = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag)
    experience_gained = models.PositiveIntegerField()


class Badge(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    # icon = models.ImageField()
    class_name = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()


class DockerManager(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.GenericIPAddressField(unique=True)
    port = models.PositiveIntegerField()
    url = models.CharField(max_length=100, default="")


class Configurations(models.Model):
    docker_managers = models.OneToOneField(DockerManager)
