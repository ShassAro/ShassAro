import json
import subprocess
from threading import Thread
from django.core import serializers

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
    def __init__(self, Shassaros, DockerServers, *args, **kw):
        self.shassarosContainer = ShassaroContainer(Shassaros)
        self.dockerServers = DockerServers

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

            # Serialize goals - Sorry for future us
            self.shassarosContainer.shassaros[0].goals = json.loads("{\"goals\":" + self.shassarosContainer.shassaros[0].goals + "}")["goals"]
            self.shassarosContainer.shassaros[0].goals = json.loads("{\"goals\":" + self.shassarosContainer.shassaros[1].goals + "}")["goals"]


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
            shassaroEnv1.append("FACTER_myusers={\"" + self.shassarosContainer.shassaros[0].participants['name'] +
                                "\" : {\"password\" : \"" +
                                self.shassarosContainer.shassaros[0].participants['password']
                                + "\"}}")

            # Populate myusers for both images (json)
            shassaroEnv2.append("FACTER_myusers={\"" + self.shassarosContainer.shassaros[1].participants['name'] +
                                "\" : {\"password\" : \"" +
                                self.shassarosContainer.shassaros[1].participants['password']
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
                                                         self.shassarosContainer.shassaros[0].participants['name'],
                                                mem_limit="256m", ports=[(5901,'tcp')], environment=shassaroEnv1,
                                                name="shassaro_"+
                                                     self.shassarosContainer.shassaros[0].participants['name'],
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
                                                         self.shassarosContainer.shassaros[1].participants['name'],
                                                mem_limit="256m", ports=[(5901,'tcp')], environment=shassaroEnv2,
                                                name="shassaro_"+
                                                     self.shassarosContainer.shassaros[1].participants['name'],
                                                command="/bin/bash",
                                                stdin_open=True,
                                                tty=True)

            # Set the container ID
            self.shassarosContainer.shassaros[1].docker_id = container['Id']

        except Exception as e:

            # Kill the shassaro instance 1
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[1].docker_id).kill()

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

            # Kill shassaro instances
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[0].docker_id).kill()
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[1].docker_id).kill()

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

            # Kill shassaro instances
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[0].docker_id).kill()
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[1].docker_id).kill()

            raise ShassAroException("Could not start image2 . Exception: " + str(e))

        # Create two threads that runs puppet
        t1 = Thread(target=self.executeDocker1)
        t2 = Thread(target=self.executeDocker2)

        # Start the threads
        t1.start()
        t2.start()

        # Wait for finish
        t1.join()
        t2.join()

        try:
            # Get local port
            localPort = self.getPortOnLocalServer()

            # Create the command
            arguments = ["nohup", "/opt/noVNC/utils/launch.sh", "--vnc",
                         "{0}:{1}".format(urlparse(self.docker_server).netloc.split(":")[0], shassaroPort1),
                        "--listen", str(localPort)]

            # Start websocket to container 1
            subprocess.Popen(arguments)
            #os.system(cmd)

            # Add it to shassaro
            self.shassarosContainer.shassaros[0].participants["vnc_port"] = localPort

        except Exception as e:

            # Kill shassaro instances
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[0].docker_id).kill()
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[1].docker_id).kill()

            raise ShassAroException("Could not start websocket to image1. Exception: " + str(e))

        try:
            # Get local port
            localPort = self.getPortOnLocalServer()


            # Create the command
            arguments = ["nohup", "/opt/noVNC/utils/launch.sh", "--vnc",
                         "{0}:{1}".format(urlparse(self.docker_server).netloc.split(":")[0], shassaroPort2),
                        "--listen", str(localPort)]

            # Start websocket to container 2
            subprocess.Popen(arguments)

            # Add it to shassaro
            self.shassarosContainer.shassaros[1].participants["vnc_port"] = localPort

        except Exception as e:

            # Kill shassaro instances
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[0].docker_id).kill()
            DockerKill(self.docker_server, self.shassarosContainer.shassaros[1].docker_id).kill()

            raise ShassAroException("Could not start websocket to image2. Exception: " + str(e))

        # Return final shassaros
        return self.shassarosContainer

    def executeDocker1(self):

        try:
            # Open a connection
            client = Client(base_url=self.docker_server, version="1.17")
            client.execute(container=self.shassarosContainer.shassaros[0].docker_id,
                           cmd="/usr/bin/puppet apply --modulepath=\"/root\" /root/shassaro.pp")

            # Start the vncserver (due to bug in the vnc puppet module)
            client.execute(container=self.shassarosContainer.shassaros[0].docker_id,
                           cmd="/sbin/service vncserver start")

        except Exception as e:
            pass

    def executeDocker2(self):

        try:
            # Open a connection
            client = Client(base_url=self.docker_server, version="1.17")
            client.execute(container=self.shassarosContainer.shassaros[1].docker_id,
                           cmd="/usr/bin/puppet apply --modulepath=\"/root\" /root/shassaro.pp")

            # Start the vncserver (due to bug in the vnc puppet module)
            client.execute(container=self.shassarosContainer.shassaros[1].docker_id,
                           cmd="/sbin/service vncserver start")

        except Exception as e:
            pass

    def getDockerServer(self):

        # Get the available docker server
        if len(self.dockerServers) == 1:

            # Only one server.. return it
            return  self.dockerServers[0]

        # If more then one:
        # Find the docker with the fewest containers.
        # Declare a minimum value
        min_containers = None
        chosen_server = None

        for docker_server in self.dockerServers:

            # Client outside of scope
            client = None
            try:
                # Open a connection
                client = Client(base_url=docker_server, version="1.17")

            except Exception as e:

                # Can't connect. pass
                pass

            try:
                # Get the number of running containers
                containers_num = len(client.containers())

                # Is there a docker server checked already?
                if min_containers == None:
                    min_containers = containers_num
                    chosen_server = docker_server

                else:
                    # Is this container has more?
                    if min_containers > containers_num:
                        min_containers = containers_num
                        chosen_server = docker_server

            except Exception as e:
                # Cant query this docker server.. skipping.
                pass

            if min_containers == None:
                raise ShassAroException("Cant connect to any of the docker server provided.")

            else:
                return chosen_server

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

        # Client out of scope
        client = None

        # Docker ip out of scope
        docker_port = None

        try:
            # Open a connection
            client = Client(base_url=self.dockerServerIp, version="1.17")

        except Exception as e:
            raise ShassAroException("Could not connect to docker API. Exception: " + str(e))

        try:
            inspect = client.inspect_container(container=self.dockerId)
            docker_port = inspect['NetworkSettings']['Ports']['5901/tcp'][0]['HostPort']

        except Exception as e:

            # Cant get the IP. Dont know the websockify query string.
            docker_port = None

        try:
            # Kill the container
            client.remove_container(container=self.dockerId, force=True)

        except Exception as e:
            raise ShassAroException("Could not kill docker. Exception: " + str(e))

        try:
            # Do we know the port?
            if (docker_port != None):

                # Create a kill command
                cmd = "pkill -9 -f \".*websockify.*{0}.*\"".format(docker_port)

                os.system(cmd)

        except Exception as e:
            raise ShassAroException("Could not shutdown websockify. Exception: " + str(e))

        return ""


class DockerScavage():

    def scavage(self):
        pass
