__author__ = 'shay'

from django.db import models

class Image(models.model):
    docker_name = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.TextField() # JSON-serialized (text) version of the tags
    level = models.PositiveIntegerField()
    allow_in_game = models.BooleanField()
    hint = models.TextField() # String with undetermined length
    goal_description = models.TextField() # String with undetermined length
    post_script_name = models.TextField() # String to represent either script name, or script path
    duration_minutes = models.PositiveIntegerField()

class LearningPath(models.model):
    subject = models.CharField(max_length=100)
    images = models.ManyToManyField(Image)
    picture = models.ImageField()
    color = models.CharField(max_length=100)
    description = models.TextField()

class GameUser(models.model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    vnc_port = models.PositiveIntegerField()

class Shassaro(models.model):
    goals = models.TextField() #JSON-serialized (text) version of the goals
    participants = models.ManyToManyField(GameUser)
    shassaro_ip = models.IPAddressField()
    docker_server_ip = models.IPAddressField()
    docker_id = models.CharField(max_length=100)

class Game(models.model):
    groups = models.TextField() # JSON-serialized (text) version of the groups
    computer = models.BooleanField()
    images = models.ManyToManyField(Image)
    shassaros = models.ManyToManyField(Shassaro)
    start_time = models.DateTimeField()
    goals_completed = models.TextField() # JSON-serialized (text) version of our completed goals
    duration_minutes = models.PositiveIntegerField()

class GameResult(models.model):
    #losing_users =
    #winning_users =
    computer = models.BooleanField()
    start_time = models.DateTimeField()
    actual_duration_minutes = models.PositiveIntegerField()
    tags = models.TextField() # JSON-serialized (text) version of the tags
    experience_gained = models.PositiveIntegerField()

class Badge(models.model):
    name = models.CharField(max_length=100)
    icon = models.ImageField()
    class_name = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()

class Configurations(models.model):
    docker_server = models.TextField() # JSON-serialized (text) version of the docker server's IPs / names
