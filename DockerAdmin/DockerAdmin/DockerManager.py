__author__ = 'roir'

from ShassAro import ShassAro
from Exceptions import *
from ShassaroContainer import ShassaroContainer

class DockerDeploy():

    def __init__(self, Shassaros, *args, **kw):
        # Initialize any variables you need from the input you get
        self.shassaros = ShassaroContainer(Shassaros)

    def deploy(self):

        return self.shassaros


class DockerKill():

    def __init__(self, dockerServerIp, dockerId):
        self.dockerServerIp = dockerServerIp
        self.dockerId = dockerId

    def kill(self):

        return ""



class DockerScavage():

    def scavage(self):
        pass



