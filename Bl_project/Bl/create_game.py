import random
from Bl_project.Bl.models import Shassaro, GameUser

__author__ = 'shay'


def generate_goal():
    """
    Generates a random hash (128 bits)
    :return: Hex value of the hash
    """
    hash_string = random.getrandbits(128)
    return '%032x' % hash_string


def generate_password():
    """
    Generates a random hash (32 bits)
    :return: Hex value of the hash
    """
    hash_string = random.getrandbits(32)  # Generate a random bit string of 32 bits
    hash_list = list('%008x' % hash_string)  # hex those random bits into a list

    # Switch 1/2 of the hex chars into special symbols
    for x in xrange(2):
        symbol_pos = random.randint(0, 7)
        which_symbol = random.choice('~!@#$%^&*()_+')
        hash_list[symbol_pos] = which_symbol

    return "".join(hash_list)

def generate_shassaro(participants, image):
    """
    Generate a Shassaro object
    :param participants: list of usernames that are to use this shassaro
    :param image: the image this shassaro will be using
    :return: the generated shassaro with goals hashes
    """
    shassaro = Shassaro()
    for participant in participants:
        game_user = GameUser()
        game_user.name = participant
        game_user.password = generate_password()
        shassaro.participants.add(game_user)

    shassaro.goals = [generate_goal() for goal in image.goal_description]
    return shassaro