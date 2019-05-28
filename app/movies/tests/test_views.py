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

    def test_movie_post_new_movie(self):
        url = reverse('movies')
        resp = self.client.post(url, {"title": "Titanic"})
        self.assertEqual(resp.status_code, 200)
        movie_dict = json.loads(resp.content)
        movie_id = movie_dict["ID"]
        movie = models.Movie.objects.get(pk=movie_id)
        self.assertEqual(movie_dict, movie.to_dict())

    def test_movie_post_update_existing_movie(self):
        url = reverse('movies')
        resp = self.client.post(url, {"title": "Titanic"})
        self.assertEqual(resp.status_code, 200)
        movie_dict = json.loads(resp.content)
        movie_id = movie_dict["ID"]
        movie = models.Movie.objects.get(pk=movie_id)

        movie.writers = "no writers"
        movie.save()

        resp = self.client.post(url, {"title": "Titanic"})
        self.assertEqual(resp.status_code, 200)
        movie_dict = json.loads(resp.content)
        movie_id = movie_dict["ID"]
        movie = models.Movie.objects.get(pk=movie_id)
        self.assertEqual(movie_dict, movie.to_dict())


class CommentsEndpointsTests(TestCase):
    fixtures = ['movies/tests/sample_data.json']

    def test_comments_list_get_no_filter(self):
        url = reverse('comments')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        comments_list = json.loads(resp.content)
        self.assertEqual(len(comments_list), 5)

    def test_comments_list_get_only_one_movie(self):
        url = reverse('comments')
        movie = models.Movie.objects.get(pk=1)
        resp = self.client.get(url, {"movieID": movie.id})
        self.assertEqual(resp.status_code, 200)
        comments_list = json.loads(resp.content)
        self.assertEqual(len(comments_list), movie.total_comments)

    def test_comments_list_non_existing_movie(self):
        url = reverse('comments')
        resp = self.client.get(url, {"movieID": 100000})
        self.assertEqual(resp.status_code, 404)

    def test_comments_post_no_text(self):
        url = reverse('comments')
        movie = models.Movie.objects.get(pk=1)
        resp = self.client.post(url, {"movieID": movie.id})
        self.assertEqual(resp.status_code, 400)

    def test_comments_post_no_movie_id(self):
        url = reverse('comments')
        resp = self.client.post(url, {"text": "No text"})
        self.assertEqual(resp.status_code, 400)

    def test_comments_post_non_existing_movie(self):
        url = reverse('comments')
        resp = self.client.post(url, {"movieID": 100000, "text": "No text"})
        self.assertEqual(resp.status_code, 404)

    def test_comments_post(self):
        url = reverse('comments')
        movie = models.Movie.objects.get(pk=1)
        resp = self.client.post(url, {"movieID": movie.id, "text": "No text"})
        self.assertEqual(resp.status_code, 200)
        comment = json.loads(resp.content)
        self.assertEqual(comment["Movie"], str(movie))
        self.assertEqual(comment["Text"], "No text")
