import json
from django.urls import reverse
from django.test import TestCase

from movies import models, views


class MoviesTests(TestCase):
    fixtures = ['movies/tests/sample_data.json']

    def test_movies_list_get(self):
        url = reverse('movies_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        movies_dict = json.loads(resp.content)
        self.assertEqual(len(movies_dict), 2)
