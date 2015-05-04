from Bl.create_game import deploy_shassaros
from Bl.bl_exceptions import DockerManagerNotAvailableError, DeployError
from Bl.models import Shassaro, GameUser, DockerManager
from LoginAPITestCase import LoginAPITestCase


__author__ = 'assaf'

from unittest import TestCase


class When_calling_deploy_shassaros_with_None(TestCase):
    def test_it_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            deploy_shassaros(None)

class When_calling_deploy_shassaros_with_not_exactly_2_args(TestCase):
    def test_it_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            deploy_shassaros((1,))


class When_calling_deploy_shassaros_with_not_Shassaro_type_args(TestCase):
    def test_it_should_raise_TypeError(self):
        with self.assertRaises(TypeError):
            deploy_shassaros((1,2,))


def create_initial_shassaro_mock():
    shassaro = Shassaro()
    shassaro.goals = ['goal1-hash','goal2-hash']
    shassaro.shassaro_ip = "0.0.0.0"
    shassaro.docker_server_ip = "0.0.0.0"
    shassaro.save()
    for i in range(2):
        game_user = GameUser()
        game_user.name = "user{0}".format(i)
        game_user.password = "Password1"
        game_user.vnc_port = 0
        game_user.save()
        shassaro.participants.add(game_user)

    return shassaro


def mock_Shassaro_objects():
    return [create_initial_shassaro_mock() for i in range(2)]


def mock_DockerManager():
    docker_manager = DockerManager()
    docker_manager.name = "Docker-Manager"
    docker_manager.ip = "127.0.0.1"
    docker_manager.port = 8000
    docker_manager.url = "docker-admin-mock"
    docker_manager.save()


class When_there_is_no_DockerManagerAvailable(TestCase):
    def test_it_should_raise_DockerManagerNotAvailableError(self):
        with self.assertRaises(DockerManagerNotAvailableError):
            deploy_shassaros(mock_Shassaro_objects())


class When_request_to_DockerManager_fails(TestCase):
    def setUp(self):
        # super(When_request_to_DockerManager_fails, self).setUp()
        self.shassaros = mock_Shassaro_objects()
        mock_DockerManager()

    def test_it_should_raise_DeployError(self):
        with self.assertRaises(DeployError):
            deploy_shassaros(self.shassaros)