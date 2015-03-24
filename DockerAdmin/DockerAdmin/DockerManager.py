__author__ = 'roir'

from ShassAro import ShassAro
from Exceptions import *
from ShassaroContainer import ShassaroContainer

class DockerDeploy():

    # Constructor
    def __init__(self, Shassaros, *args, **kw):
        self.shassaros = ShassaroContainer(Shassaros)

    # The actual deploy function
    def deploy(self):

        """
        Give users as "export FACTER_myusers=json when json: {"user1" : {"password" : "Password1"}, "user2" : {"password" : "Password2"}}
        Give all facters as "export FACTER_goal1=goal" ,,
        Give all remote facters as "export FACTER_remoteGoal1=goal"
        """

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



