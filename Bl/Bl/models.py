from django.contrib.auth.models import User
from jsonfield import JSONField

__author__ = 'shay'

from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()

class Image(models.Model):
    docker_name = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    level = models.PositiveIntegerField()
    allow_in_game = models.BooleanField()
    hints = JSONField() # represented as a json array
    goal_description = models.TextField() # String with undetermined length
    post_script_name = models.TextField() # String to represent either script name, or script path
    duration_minutes = models.PositiveIntegerField()

class LearningPath(models.Model):
    subject = models.CharField(max_length=100)
    images = models.ManyToManyField(Image)
    # picture = models.ImageField()
    color = models.CharField(max_length=100)
    description = models.TextField()

class GameUser(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    vnc_port = models.PositiveIntegerField()

class Shassaro(models.Model):
    goals = JSONField() #models.TextField() #JSON-serialized (text) version of the goals
    participants = models.ManyToManyField(GameUser)
    shassaro_ip = models.IPAddressField()
    docker_server_ip = models.IPAddressField()
    docker_id = models.CharField(max_length=100)

class Game(models.Model):
    group1 = models.ManyToManyField(User, related_name='group1')
    group2 = models.ManyToManyField(User, related_name='group2')
    computer = models.BooleanField()
    images = models.ManyToManyField(Image)
    shassaros = models.ManyToManyField(Shassaro)
    start_time = models.DateTimeField()
    goals_completed = JSONField()
    duration_minutes = models.PositiveIntegerField()

class GameResult(models.Model):
    losing_users = models.ManyToManyField(User, related_name='losing_users')
    winning_users = models.ManyToManyField(User, related_name='winning_users')
    computer = models.BooleanField()
    start_time = models.DateTimeField()
    actual_duration_minutes = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag)
    experience_gained = models.PositiveIntegerField()

class Badge(models.Model):
    name = models.CharField(max_length=100)
    # icon = models.ImageField()
    class_name = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()

class DockerServer(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    ip = models.IPAddressField()

class Configurations(models.Model):
    docker_server = models.ManyToManyField(DockerServer)
