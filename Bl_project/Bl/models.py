from django.contrib.auth.models import User
from jsonfield import JSONField
from django.db import models


class Quotes(models.Model):
    quote = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()


class Image(models.Model):
    docker_name = models.CharField(max_length=100, primary_key=True)
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
    vnc_port = models.PositiveIntegerField(null=True)


class Shassaro(models.Model):
    goals = JSONField()  # JSON-serialized (text) version of the goals
    participants = models.ManyToManyField(GameUser)
    shassaro_ip = models.GenericIPAddressField(null=True)
    docker_server_ip = models.GenericIPAddressField(null=True)
    docker_id = models.CharField(max_length=100, null=True)
    docker_name = models.CharField(max_length=1000, null=True)
    goals_completed = JSONField(null=True)

class GameRequestStatus(models.Model):
    status = models.CharField(max_length=100, primary_key=True)
    message = models.CharField(max_length=1000)


class Game(models.Model):
    userA = models.CharField(max_length=100)
    userB = models.CharField(max_length=100)
    computer = models.BooleanField(default=False)
    images = models.ManyToManyField(Image)
    shassaros = models.ManyToManyField(Shassaro)
    start_time = models.DateTimeField(null=True)
    duration_minutes = models.PositiveIntegerField(null=True)


class GameRequest(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    tags = models.ManyToManyField(Tag)
    submitted_at = models.DateTimeField()
    status = models.ForeignKey(GameRequestStatus)
    game = models.ManyToManyField(Game)


class GameResult(models.Model):
    losing_users = models.ManyToManyField(User, related_name='losing_users')
    winning_users = models.ManyToManyField(User, related_name='winning_users')
    computer = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    actual_duration_minutes = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag)
    experience_gained = models.PositiveIntegerField()
    game_timed_out = models.BooleanField(default=False)


class Badge(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    # icon = models.ImageField()
    class_name = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()


class DockerManager(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.GenericIPAddressField(unique=True)
    port = models.PositiveIntegerField()
    url = models.CharField(max_length=100, default="/")


class DockerServer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    protocol = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(unique=True)
    port = models.PositiveIntegerField()
