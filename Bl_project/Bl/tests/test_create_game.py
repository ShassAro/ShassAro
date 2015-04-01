"""

from unittest import TestCase
from Bl_project.Bl.create_game import deploy_shassaros
from Bl_project.Bl.exceptions import *

__author__ = 'assaf'


class when_calling_deploy_shassaros_with_invalid_data(TestCase):
    def it_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            deploy_shassaros(None)

"""