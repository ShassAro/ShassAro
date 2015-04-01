from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from test_tag_class import TagTests
from test_badge_class import BadgeTests


__author__ = 'shay'


class ImageTests(APITestCase):
    def create_image(self, docker_name, description, tags, level, allow_in_game, hints, goal_description,
                     post_script_name, duration_minutes):
        """
        Get all Image fields and use them to create the request_data json.
        Take that request_data and post it to /images/.
        Return both the request_data and the response from performing the post.
        """
        request_data = {"docker_name": docker_name, "description": description, "tags": [tags], "level": level,
                        "allow_in_game": allow_in_game, "hints": hints, "goal_description": goal_description,
                        "post_script_name": post_script_name, "duration_minutes": duration_minutes}
        return request_data, self.client.post('/images/', request_data, format='json')



    def test_image_create(self):
        """
        Ensure we can create a couple of Images (the correct way)
        """
        request_data = {"name": "tag1", "description": "tag1_desc"}
        request_data, self.client.post('/tags/', request_data, format='json')

        request_data, response = self.create_image("docker1",
                                                   "Best Docker!",
                                                   reverse('tag-detail', args={'tag1'}),
                                                   100,
                                                   True,
                                                   {"hint1": "hintush"},
                                                   {"goal1": "Best goal"},
                                                   "post_script1",
                                                   60)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertDictContainsSubset(request_data, response.data)