
#from unittest import TestCase
from rest_framework.test import APITestCase
#from Bl_project.Bl.create_game import deploy_shassaros
import Bl_project.Bl.create_game

__author__ = 'assaf'

"""
class when_calling_deploy_shassaros_with_invalid_data(APITestCase):
    def test_it_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            deploy_shassaros(None)

"""

class AssafTest(APITestCase):
    def test_blah(self):
        print 'ASD'