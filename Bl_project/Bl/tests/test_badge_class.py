from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


__author__ = 'shay'


class BadgeTests(APITestCase):
    def create_badge(self, name, class_name, experience):
        """
        Get a name, class_name, and experience, and use them to create the request_data json.
        Take that request_data and post it to /badges/.
        Return both the request_data and the response from performing the post.
        """
        request_data = {"name": name, "class_name": class_name, "experience": experience}
        response = self.client.post('/badges/', request_data, format='json')
        return request_data, response

    def test_badge_create(self):
        """
        Make sure we can create a couple of badges (the correct way)
        """
        request_data, response = self.create_badge("badge1", "Badass Badge", 100)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(request_data, response.data)

        request_data, response = self.create_badge("badge2", "Better Badge", 200)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(request_data, response.data)

        """
        Verify Badge.name field is unique
        """
        request_data, response = self.create_badge("badge1", "New Badge", 300)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'name': [u'This field must be unique.']})

        """
        Verify Badge.class_name and Badge.experience does not have to be unique
        """
        request_data, response = self.create_badge("badge3", "New Badge", 300)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(request_data, response.data)

        """
        Verify Badge.experience accepts numbered strings
        """
        request_data, response = self.create_badge("badge4", "New Badge", "400")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """
        Verify Badge.experience does not accept normal strings
        """
        request_data, response = self.create_badge("badge5", "New Badge", "blah")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'experience': [u'A valid integer is required.']})

        """
        Send a GET request to make sure all 4 badges appear on our DB
        """
        response = self.client.get(reverse('badge-list'))
        self.assertTrue(response.content.count('\"name\"') == 4)

        """
        Send a GET request for 'badge1'
        """
        response = self.client.get(reverse('badge-detail', args={'badge1'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'name': 'badge1'}, response.data)