import random
import json

__author__ = 'shay'

def randomize_goal():
    # Generate a random bit string of 128 bits
    hash = random.getrandbits(128)
    # hex those random bits and return
    return '%032x' % hash

def randomize_password():
    # Generate a random bit string of 32 bits
    hash = random.getrandbits(32)
    # hex those random bits into a list
    hash_list = list('%008x' % hash)

    # Switch 1/2 of the hex chars into special symbols
    for x in xrange(2):
        symbol_pos = random.randint(0, 7)
        which_symbol = random.choice('~!@#$%^&*()_+')
        hash_list[symbol_pos] = which_symbol

    # return the list as a string
    return "".join(hash_list)

def randomize_vnc_port():
    # Generate a random 5 digit number, max 40k
    port = random.randint(10000,40000)
    return port

def game_post(json_str):
    json_data = json.loads(json_str)
    image1 = json_data["images"]["image1"]
    image2 = json_data["images"]["image2"]

    #print Image.objects.filter(docker_name = image1)
    print image1, image2

if __name__ == '__main__':
    print randomize_goal()
    print randomize_password()
    print randomize_vnc_port()
    game_post('{ "groups": { "group1": { "user1": "g1u1", "user2": "g1u2" }, "group2": { "user1": "g2u1", "user2": "g2u2" } }, "images": { "image1": "docker-test", "image2": "image2_name" } }')


"""
class Shassaro(models.Model):
    goals = JSONField() #JSON-serialized (text) version of the goals
    participants = models.ManyToManyField(GameUser)
    shassaro_ip = models.IPAddressField()
    docker_server_ip = models.IPAddressField()
    docker_id = models.CharField(max_length=100)

class GameUser(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    vnc_port = models.PositiveIntegerField()

class Game(models.Model):
    group1 = models.ManyToManyField(User, related_name='group1')
    group2 = models.ManyToManyField(User, related_name='group2')
    computer = models.BooleanField(default=False)
    images = models.ManyToManyField(Image)
    shassaros = models.ManyToManyField(Shassaro)
    start_time = models.DateTimeField()
    goals_completed = JSONField()
    duration_minutes = models.PositiveIntegerField()

class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()

class Image(models.Model):
    docker_name = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    level = models.PositiveIntegerField()
    allow_in_game = models.BooleanField(default=False)
    hints = JSONField() # represented as a json array
    goal_description = models.JSONField() # JSON describing the goals in this image
    post_script_name = models.TextField() # String to represent either script name, or script path
    duration_minutes = models.PositiveIntegerField()
"""