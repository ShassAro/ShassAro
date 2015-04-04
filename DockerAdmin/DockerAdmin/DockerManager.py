__author__ = 'roir'

from ShassAro import ShassAro
from Exceptions import *
from ShassaroContainer import ShassaroContainer
from docker import Client
import hashlib
from random import randint
import socket
from urlparse import urlparse
import os

class DockerDeploy():

    # Constructor
    def __init__(self, Shassaros, *args, **kw):
        self.shassarosContainer = ShassaroContainer(Shassaros)

    # The actual deploy function
    def deploy(self):

        """
        Give users as "export FACTER_myusers=json when json: {"user1" : {"password" : "Password1"}, "user2" : {"password" : "Password2"}}
        Give all facters as "export FACTER_goal1=goal" ,,
        Give all remote facters as "export FACTER_remoteGoal1=goal"
        """

        # Figure out the docker server
        self.docker_server = self.getDockerServer()

        # Set it to shassaro
        self.shassarosContainer.shassaros[0].docker_server_ip = self.docker_server
        self.shassarosContainer.shassaros[1].docker_server_ip = self.docker_server

        # Declare the client out of scope
        client = None

        # Create the environment varialbes
        shassaroEnv1 = []
        shassaroEnv2 = []

        # Create placeholders for ports
        shassaroPort1 = ""
        shassaroPort2 = ""

        try:
            # Initialize counter
            counter=1

            # Populate goal environment variables for image1
            for currGoal in self.shassarosContainer.shassaros[0].goals:
                shassaroEnv1.append("FACTER_goal" + str(counter) + "=" + currGoal)
                counter+=1

            # Restart counter
            counter=1

            # Populate goal environment variables for image1
            for currGoal in self.shassarosContainer.shassaros[1].goals:
                shassaroEnv2.append("FACTER_goal" + str(counter) + "=" + currGoal)
                counter+=1

            # Populate myusers for both images (json)
            shassaroEnv1.append("FACTER_myusers={\"" + self.shassarosContainer.shassaros[0].participants[0]['name'] +
                                "\" : {\"password\" : \"" +
                                self.shassarosContainer.shassaros[0].participants[0]['password']
                                + "\"}}")

            # Populate myusers for both images (json)
            shassaroEnv2.append("FACTER_myusers={\"" + self.shassarosContainer.shassaros[1].participants[0]['name'] +
                                "\" : {\"password\" : \"" +
                                self.shassarosContainer.shassaros[1].participants[0]['password']
                                + "\"}}")

        except Exception as e:
            raise ShassAroException("Could not parse goals parameters. Exception: " + str(e))

        try:
            # Open a connection
            client = Client(base_url=self.docker_server, version="1.17")

        except Exception as e:
            raise ShassAroException("Could not connect to docker API. Exception: " + str(e))

        try:
            # Create container 1
            container = client.create_container(image=self.shassarosContainer.shassaros[0].docker_name,
                                                hostname="shassaro_"+
                                                         self.shassarosContainer.shassaros[0].participants[0]['name'],
                                                mem_limit="256m", ports=[(5901,'tcp')], environment=shassaroEnv1,
                                                name="shassaro_"+
                                                     self.shassarosContainer.shassaros[0].participants[0]['name'],
                                                command="/bin/bash",
                                                stdin_open=True,
                                                tty=True)

            # Set the container ID
            self.shassarosContainer.shassaros[0].docker_id = container['Id']

        except Exception as e:
            raise ShassAroException("Could not Create shassaro image1 . Exception: " + str(e))

        try:
            # Create container 2
            container = client.create_container(image=self.shassarosContainer.shassaros[1].docker_name,
                                                hostname="shassaro_"+
                                                         self.shassarosContainer.shassaros[1].participants[0]['name'],
                                                mem_limit="256m", ports=[(5901,'tcp')], environment=shassaroEnv2,
                                                name="shassaro_"+
                                                     self.shassarosContainer.shassaros[1].participants[0]['name'],
                                                command="/bin/bash",
                                                stdin_open=True,
                                                tty=True)

            # Set the container ID
            self.shassarosContainer.shassaros[1].docker_id = container['Id']

        except Exception as e:

            # TODO: clean shassaro 1
            raise ShassAroException("Could not Create shassaro image2 . Exception: " + str(e))

        try:
            # Start container 1
            client.start(container=self.shassarosContainer.shassaros[0].docker_id,
                         publish_all_ports=True)

            # Get the IP of the container
            inspect = client.inspect_container(container=self.shassarosContainer.shassaros[0].docker_id)
            self.shassarosContainer.shassaros[0].shassaro_ip = inspect.get("NetworkSettings").get("IPAddress")
            shassaroPort1 = inspect['NetworkSettings']['Ports']['5901/tcp'][0]['HostPort']

        except Exception as e:

            # TODO: clean shassaro 1 and 2
            raise ShassAroException("Could not start image1 . Exception: " + str(e))

        try:
            # Start container 2
            client.start(container=self.shassarosContainer.shassaros[1].docker_id,
                         publish_all_ports=True)

            # Get the IP of the container
            inspect = client.inspect_container(container=self.shassarosContainer.shassaros[1].docker_id)
            self.shassarosContainer.shassaros[1].shassaro_ip = inspect.get("NetworkSettings").get("IPAddress")
            shassaroPort2 = inspect['NetworkSettings']['Ports']['5901/tcp'][0]['HostPort']

        except Exception as e:

            # TODO: stop shassaro 1
            # TODO: clean shassaro 1 and 2
            raise ShassAroException("Could not start image2 . Exception: " + str(e))

        try:
            # Run puppet on container 1
            client.execute(container=self.shassarosContainer.shassaros[0].docker_id,
                           cmd="/usr/bin/puppet apply --modulepath=\"/root\" /root/shassaro.pp")

            # Start the vncserver (due to bug in the vnc puppet module)
            client.execute(container=self.shassarosContainer.shassaros[0].docker_id,
                           cmd="/sbin/service vncserver start")


        except Exception as e:

            # TODO: stop shassaro 1 and 2
            # TODO: clean shassaro 1 and 2
            raise ShassAroException("Could not run puppet on image1. Exception: " + str(e))

        try:
             # Run puppet on container 1
            client.execute(container=self.shassarosContainer.shassaros[1].docker_id,
                           cmd="/usr/bin/puppet apply --modulepath=\"/root\" /root/shassaro.pp")

            # Start the vncserver (due to bug in the vnc puppet module)
            client.execute(container=self.shassarosContainer.shassaros[1].docker_id,
                           cmd="/sbin/service vncserver start")

        except Exception as e:

            # TODO: stop shassaro 1 and 2
            # TODO: clean shassaro 1 and 2
            raise ShassAroException("Could not run puppet on image2. Exception: " + str(e))

        try:
            # Get local port
            localPort = self.getPortOnLocalServer()

            # Create the command
            cmd = "/opt/noVNC/utils/launch.sh --vnc {0}:{1} --listen {2} &".format(
                urlparse(self.docker_server).netloc.split(":")[0], shassaroPort1, localPort)

            # Start websocket to container 1
            os.system(cmd)

            # Add it to shassaro
            self.shassarosContainer.shassaros[0].participants[0]["vnc_port"] = localPort

        except Exception as e:

            # TODO: stop shassaro 1 and 2
            # TODO: clean shassaro 1 and 2
            raise ShassAroException("Could not start websocket to image1. Exception: " + str(e))

        try:
            # Get local port
            localPort = self.getPortOnLocalServer()

            # Create the command
            cmd = "/opt/noVNC/utils/launch.sh --vnc {0}:{1} --listen {2} &".format(
                urlparse(self.docker_server).netloc.split(":")[0], shassaroPort2, localPort)

            # Start websocket to container 1
            os.system(cmd)

            # Add it to shassaro
            self.shassarosContainer.shassaros[1].participants[0]["vnc_port"] = localPort

        except Exception as e:

            # TODO: stop websocket to image 1
            # TODO: stop shassaro 1 and 2
            # TODO: clean shassaro 1 and 2
            raise ShassAroException("Could not start websocket to image2. Exception: " + str(e))


        # Return final shassaros
        return self.shassarosContainer


    def getDockerServer(self):

        # Get the available docker server

        # If more then one:
        # Find the docker with the fewest containers

        # Return it
        return "http://127.0.0.1:4243"

    def getPortOnDockerServer(self):

        toSearch = True
        tempPort = None

        # Parse only the IP out of the url
        dockerIp =  urlparse(self.docker_server).netloc.split(":")[0]

        while (toSearch):

            # Generate a random port number
            tempPort = randint(10000, 40000)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((dockerIp, tempPort))

            if result != 0:
                # Port is not open!
                toSearch = False

        return tempPort

    def getPortOnLocalServer(self):

        toSearch = True
        tempPort = None

        while (toSearch):

            # Generate a random port number
            tempPort = randint(10000, 40000)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(("127.0.0.1", tempPort))

            if result != 0:
                # Port is not open!
                toSearch = False

        return tempPort

class DockerKill():

    def __init__(self, dockerServerIp, dockerId):
        self.dockerServerIp = dockerServerIp
        self.dockerId = dockerId

    def kill(self):
        return ""


class DockerScavage():

    def scavage(self):
        pass



