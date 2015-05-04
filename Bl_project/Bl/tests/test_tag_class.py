from Bl.tests.LoginAPITestCase import LoginAPITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


__author__ = 'shay'


class TagTests(LoginAPITestCase):

    #def runTest(self):
    #    pass

    def create_tag(self, name, description):
        """
        Get a name and a description, and use them to create the request_data json.
        Take that request_data and post it to /tags/.
        Return both the request_data and the response from performing the post.
        """
        request_data = {"name": name, "description": description}
        return request_data, self.client.post('/tags/', request_data, format='json')

    def test_tag_create(self):
        """
        Ensure we can create a couple of tags (the correct way)
        """
        request_data, response = self.create_tag("tag1", "tag1_desc")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(request_data, response.data)

        request_data, response = self.create_tag("tag2", "tag2_desc")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(request_data, response.data)

        """
        Verify Tag.name field is unique
        """
        request_data, response = self.create_tag("tag1", "tag1_desc")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'name': [u'This field must be unique.']})

        """
        Verify Tag.description does not have to be unique
        """
        request_data, response = self.create_tag("tag3", "tag1_desc")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(request_data, response.data)

        """
        Send a GET request to make sure all 3 tags appear on our DB
        """
        response = self.client.get(reverse('tag-list'))
        self.assertTrue(response.content.count('name') == 3)

        """
        Send a GET request for 'tag1'
        """
        response = self.client.get(reverse('tag-detail', args={'tag1'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'name': 'tag1'}, response.data)