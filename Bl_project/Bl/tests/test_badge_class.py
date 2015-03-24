from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


__author__ = 'shay'


class BadgeTests(APITestCase):
    def test_badge_create(self):
        """
        Make sure we can create a couple of badges (the correct way)
        """
        data = {"name": "badge1", "class_name": "Badass Badge", "experience": 100}
        response = self.client.post('/badges/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(data, response.data)

        data = {"name": "badge2", "class_name": "Better Badge", "experience": 200}
        response = self.client.post('/badges/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(data, response.data)

        """
        Verify Badge.name field is unique
        """
        data = {"name": "badge1", "class_name": "New Badge", "experience": 300}
        response = self.client.post('/badges/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'name': [u'This field must be unique.']})

        """
        Verify Badge.class_name and Badge.experience does not have to be unique
        """
        data = {"name": "badge3", "class_name": "New Badge", "experience": 300}
        response = self.client.post('/badges/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(data, response.data)

        """
        Verify Badge.experience accepts numbered strings
        """
        data = {"name": "badge4", "class_name": "New Badge", "experience": "400"}
        response = self.client.post('/badges/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """
        Verify Badge.experience does not accept normal strings
        """
        data = {"name": "badge5", "class_name": "New Badge", "experience": "blah"}
        response = self.client.post('/badges/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'experience': [u'A valid integer is required.']})