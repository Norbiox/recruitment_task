import json
from django.urls import reverse
from django.test import TestCase

from movies import models, views


class MoviesEndpointsTests(TestCase):
    fixtures = ['movies/tests/sample_data.json']

    def test_movies_list_get(self):
        url = reverse('movies')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        movies_list = json.loads(resp.content)
        self.assertEqual(len(movies_list), 2)

    def test_movie_post_no_title(self):
        url = reverse('movies')
        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, 400)

    def test_movie_post_non_existing_movie(self):
        url = reverse('movies')
        resp = self.client.post(url, {"title": ""})
        self.assertEqual(resp.status_code, 200)
        movie_dict = json.loads(resp.content)
        self.assertEqual(movie_dict, {})

    def test_movie_post(self):
        url = reverse('movies')
        resp = self.client.post(url, {"title": "Titanic"})
        self.assertEqual(resp.status_code, 200)
        movie_dict = json.loads(resp.content)
        movie_id = movie_dict["id"]
        movie = models.Movie.objects.get(pk=movie_id)
        self.assertEqual(movie_dict, movie.to_dict())

