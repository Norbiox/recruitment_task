import json
import pytz
from datetime import datetime
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
        self.assertEqual(len(comments_list), movie.get_total_comments())

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


class TopEndpointTests(TestCase):
    fixtures = ['movies/tests/sample_data.json']

    def test_top_no_filter(self):
        url = reverse('top')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        top_list = json.loads(resp.content)
        self.assertEqual(top_list, [
            {
                "movie_id": 1,
                "total_comments": 3,
                "rank": 1
            },
            {
                "movie_id": 2,
                "total_comments": 2,
                "rank": 2
            }
        ])

    def test_top_no_filter_equal_ranks(self):
        url = reverse('top')
        movie = models.Movie.objects.get(pk=2)
        models.Comment(movie=movie, text="No text").save()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        top_list = json.loads(resp.content)
        self.assertEqual(top_list, [
            {
                "movie_id": 1,
                "total_comments": 3,
                "rank": 1
            },
            {
                "movie_id": 2,
                "total_comments": 3,
                "rank": 1
            }
        ])

    def test_top_newest_comments(self):
        url = reverse('top')
        movies = models.Movie.objects.all()
        for comment in models.Comment.objects.all():
            comment.created=datetime(2000, 1, 1, tzinfo=pytz.utc)
            comment.save()
        models.Comment(
            movie=movies[0], text="No text",
            created=datetime(2018, 1, 1, tzinfo=pytz.utc)
        ).save()
        comment1 = models.Comment(
            movie=movies[0], text="No text",
            created=datetime(2018, 1, 1, tzinfo=pytz.utc)
        ).save()
        comment2 = models.Comment(
            movie=movies[1], text="No text",
            created=datetime(2018, 1, 1, tzinfo=pytz.utc)
        ).save()
        resp = self.client.get(url, {
            'begin_date': '2017-05-28'
        })
        self.assertEqual(resp.status_code, 200)
        top_list = json.loads(resp.content)
        self.assertEqual(top_list, [
            {
                "movie_id": 1,
                "total_comments": 2,
                "rank": 1
            },
            {
                "movie_id": 2,
                "total_comments": 1,
                "rank": 2
            }
        ])

    def test_top_oldest_comments(self):
        url = reverse('top')
        movies = models.Movie.objects.all()
        for comment in models.Comment.objects.all():
            comment.created=datetime(2000, 1, 1, tzinfo=pytz.utc)
            comment.save()
        models.Comment(
            movie=movies[0], text="No text",
            created=datetime(2018, 1, 1, tzinfo=pytz.utc)
        ).save()
        comment1 = models.Comment(
            movie=movies[0], text="No text",
            created=datetime(2018, 1, 1, tzinfo=pytz.utc)
        ).save()
        comment2 = models.Comment(
            movie=movies[1], text="No text",
            created=datetime(2018, 1, 1, tzinfo=pytz.utc)
        ).save()
        resp = self.client.get(url, {
            'end_date': '2005-05-28'
        })
        self.assertEqual(resp.status_code, 200)
        top_list = json.loads(resp.content)
        self.assertEqual(top_list, [
            {
                "movie_id": 1,
                "total_comments": 3,
                "rank": 1
            },
            {
                "movie_id": 2,
                "total_comments": 2,
                "rank": 2
            }
        ])


    def test_top_movies_with_no_comments(self):
        url = reverse('top')
        models.Movie(title="New Movie", response="True", imdb_id="0000").save()
        models.Movie(title="New Movie 2", response="True", imdb_id="00").save()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        top_list = json.loads(resp.content)
        self.assertEqual(top_list, [
            {
                "movie_id": 1,
                "total_comments": 3,
                "rank": 1
            },
            {
                "movie_id": 2,
                "total_comments": 2,
                "rank": 2
            },
            {
                "movie_id": 3,
                "total_comments": 0,
                "rank": 3
            },
            {
                "movie_id": 4,
                "total_comments": 0,
                "rank": 3
            }
        ])

