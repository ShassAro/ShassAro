__author__ = 'roir'

from ShassAro import ShassAro
from Exceptions import *
from ShassaroContainer import ShassaroContainer

class DockerDeploy():

    def __init__(self, Shassaros, *args, **kw):
        # Initialize any variables you need from the input you get
        self.shassaros = ShassaroContainer(Shassaros)

    def deploy(self):


        # Do what need to be done

        # Return shassaro instances
        #result = self.shassaros.__dict__

        #a = {}

        #a["shassaro"]= self.shassaros
        #return a


        return self.shassaros


class DockerKill(object):
    def kill(self):
        pass


class DockerScavage(object):

    def scavage(self):
        pass



