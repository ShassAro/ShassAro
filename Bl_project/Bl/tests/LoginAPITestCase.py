from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class LoginAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_superuser(username="testuser",email="bla@bla.blom", password="12345678")
        self.client.force_authenticate(user=user)
