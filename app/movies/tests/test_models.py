import json
from datetime import date
from django.test import TestCase

from movies import models


class MovieTest(TestCase):
    fixtures = ['movies/tests/sample_data.json']
    json_file = 'movies/tests/titanic.json'

    def test_str(self):
        movie = models.Movie.objects.get(title="Shrek")
        self.assertEqual(str(movie), "Shrek")

    def test_total_comments(self):
        movie = models.Movie.objects.get(title="Shrek")
        self.assertEqual(movie.total_comments, 3)

    def test_to_dict_full_info_movie(self):
        movie = models.Movie.objects.get(title="Shrek")
        movie_dict = movie.to_dict()
        self.assertIsInstance(movie_dict, dict)
        self.assertIsInstance(movie_dict["ID"], int)
        self.assertEqual(movie_dict["Title"], "Shrek")
        self.assertEqual(movie_dict["Year"], 2001)
        self.assertEqual(movie_dict["Rated"], "PG")
        self.assertEqual(movie_dict["Released"], "18 May 2001")
        self.assertEqual(movie_dict["Runtime"], "90 min")
        self.assertIsInstance(movie_dict["Genre"], str)
        self.assertEqual(movie_dict["Genre"],
                         "Animation, Adventure, Comedy, Family, Fantasy")
        self.assertIsInstance(movie_dict["Director"], str)
        self.assertIn("Andrew Adamson", movie_dict["Director"])
        self.assertIn("Vicky Jenson", movie_dict["Director"])
        self.assertIsInstance(movie_dict["Writer"], str)
        self.assertIn("William Steig (based upon the book by)",
                      movie_dict["Writer"])
        self.assertIn("Ted Elliot", movie_dict["Writer"])
        self.assertIsInstance(movie_dict["Actors"], str)
        for actor in ["Mike Myers", "Eddie Murphy", "Cameron Diaz",
                      "John Lithgow"]:
            self.assertIn(actor, movie_dict["Actors"])
        self.assertEqual(movie_dict["Plot"], "A mean lord exiles fairytale" +
                         " creatures to the swamp of a grumpy ogre, who must" +
                         " go on a quest and rescue a princess for the lord" +
                         " in order to get his land back.")
        self.assertEqual(movie_dict["Language"], "English")
        self.assertEqual(movie_dict["Country"], "USA")
        self.assertEqual(movie_dict["Awards"],
                         "Won 1 Oscar. Another 36 wins & 60 nominations.")
        self.assertEqual(movie_dict["Poster"],
                         "https://m.media-amazon.com/images/M/MV5BOGZhM2FhNT" +
                         "ItODAzNi00YjA0LWEyN2UtNjJlYWQzYzU1MDg5L2ltYWdlL2lt" +
                         "YWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg")
        self.assertIsInstance(movie_dict["Ratings"], list)
        self.assertEqual(movie_dict["Metascore"], 84)
        self.assertEqual(movie_dict["imdbRating"], 7.9)
        self.assertEqual(movie_dict["imdbVotes"], "560,926")
        self.assertEqual(movie_dict["imdbID"], "tt0126029")
        self.assertEqual(movie_dict["Type"], "movie")
        self.assertEqual(movie_dict["DVD"], "02 Nov 2001")
        self.assertEqual(movie_dict["BoxOffice"], "$266,982,666")
        self.assertEqual(movie_dict["Production"], "Dreamworks")
        self.assertEqual(movie_dict["Website"], "http://www.shrek.com/")
        self.assertEqual(movie_dict["Response"], "True")

    def test_to_dict_lack_of_info_movie(self):
        movie = models.Movie.objects.get(title="Who knows")
        movie_dict = movie.to_dict()
        self.assertIsInstance(movie_dict, dict)
        self.assertIsInstance(movie_dict["ID"], int)
        self.assertEqual(movie_dict["Title"], "Who knows")
        self.assertEqual(movie_dict["Year"], "N/A")
        self.assertEqual(movie_dict["Rated"], "N/A")
        self.assertEqual(movie_dict["Released"], "N/A")
        self.assertEqual(movie_dict["Runtime"], "N/A")
        self.assertEqual(movie_dict["Genre"], "N/A")
        self.assertEqual(movie_dict["Director"], "N/A")
        self.assertEqual(movie_dict["Writer"], "N/A")
        self.assertEqual(movie_dict["Actors"], "N/A")
        self.assertEqual(movie_dict["Plot"], "N/A")
        self.assertEqual(movie_dict["Language"], "N/A")
        self.assertEqual(movie_dict["Country"], "N/A")
        self.assertEqual(movie_dict["Awards"], "N/A")
        self.assertEqual(movie_dict["Poster"], "N/A")
        self.assertIsInstance(movie_dict["Ratings"], list)
        self.assertEqual(movie_dict["Metascore"], "N/A")
        self.assertEqual(movie_dict["imdbRating"], "N/A")
        self.assertEqual(movie_dict["imdbVotes"], "N/A")
        self.assertEqual(movie_dict["imdbID"], "qwerty123")
        self.assertEqual(movie_dict["Type"], "N/A")
        self.assertEqual(movie_dict["DVD"], "N/A")
        self.assertEqual(movie_dict["BoxOffice"], "N/A")
        self.assertEqual(movie_dict["Production"], "N/A")
        self.assertEqual(movie_dict["Website"], "N/A")
        self.assertEqual(movie_dict["Response"], "True")

    def test_from_dict_full_info_movie(self):
        with open(self.json_file) as json_file:
            data = json.load(json_file)
        movie = models.Movie.from_dict(data)
        self.assertEqual(movie.title, data["Title"])
        self.assertEqual(len(movie.ratings.all()), 3)
        self.assertEqual(movie.ratings.all()[0].movie, movie)
        self.assertEqual(movie.released, date(1997, 12, 19))
        self.assertEqual(movie.metascore, 75)
        self.assertEqual(movie.box_office, None)
        self.assertEqual(movie.dvd, date(2012, 9, 10))

    def test_from_dict_lack_of_info_movie(self):
        data = {
            "Title": "Titanic",
            "imdbID": "tt0120338",
            "Response": "True",
            "Ratings": []
        }
        movie = models.Movie.from_dict(data)
        self.assertEqual(movie.title, data["Title"])
        self.assertEqual(len(movie.ratings.all()), 0)
        self.assertEqual(movie.released, None)
        self.assertEqual(movie.metascore, None)
        self.assertEqual(movie.box_office, None)
        self.assertEqual(movie.dvd, None)

    def test_from_dict_with_save(self):
        data = {
            "Title": "Titanic",
            "imdbID": "tt0120338",
            "Response": "True",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.8/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "89%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "75/100"
                }
            ]
        }
        movies_objects_number = len(models.Movie.objects.all())
        ratings_objects_number = len(models.MovieRating.objects.all())
        movie = models.Movie.from_dict(data)
        movie.save()
        self.assertEqual(len(models.Movie.objects.all()),
                         movies_objects_number + 1)
        self.assertEqual(len(models.MovieRating.objects.all()),
                         ratings_objects_number + 3)


class CommentTest(TestCase):
    fixtures = ['movies/tests/sample_data.json']

    def test_from_dict(self):
        movie = models.Movie.objects.get(title="Who knows")
        data = {
            "movieID": movie.id,
            "text": "New comment under movie"
        }
        comment = models.Comment.from_dict(data)
        self.assertEqual(comment.text, data["text"])
        self.assertEqual(comment.movie, movie)
        self.assertEqual(comment.created.date(), date.today())

    def test_to_dict(self):
        comment = models.Comment.objects.get(text="Very well")
        comment_dict = comment.to_dict()
        self.assertIsInstance(comment_dict, dict)
        self.assertIsInstance(comment_dict["ID"], int)
        self.assertEqual(comment_dict["Movie"], "Shrek")
        self.assertEqual(comment_dict["Text"], "Very well")

    def test_str(self):
        comment = models.Comment.objects.get(text="Very well")
        self.assertEqual(str(comment), "Very well")


class MovieRatingTest(TestCase):
    fixtures = ['movies/tests/sample_data.json']

    def test_from_dict(self):
        movie = models.Movie.objects.get(title="Who knows")
        data = {
            "movieID": movie.id,
            "Source": "Rating source",
            "Value": "some value"
        }
        rating = models.MovieRating.from_dict(data)
        self.assertEqual(rating.movie, movie)
        self.assertEqual(rating.source, data["Source"])
        self.assertEqual(rating.value, data["Value"])

    def test_to_dict(self):
        rating = models.MovieRating.objects.get(value="88%")
        rating_dict = rating.to_dict()
        self.assertIsInstance(rating_dict, dict)
        self.assertEqual(len(rating_dict), 4)
        self.assertIsInstance(rating_dict["ID"], int)
        self.assertEqual(rating_dict["Movie"], "Shrek")
        self.assertEqual(rating_dict["Source"], "Rotten Tomatoes")
        self.assertEqual(rating_dict["Value"], "88%")

    def test_to_dict_short(self):
        rating = models.MovieRating.objects.get(value="88%")
        rating_dict = rating.to_dict(short=True)
        self.assertIsInstance(rating_dict, dict)
        self.assertEqual(len(rating_dict), 2)
        self.assertEqual(rating_dict["Source"], "Rotten Tomatoes")
        self.assertEqual(rating_dict["Value"], "88%")

    def test_str(self):
        rating = models.MovieRating.objects.get(value="88%")
        self.assertEqual(str(rating), "Rotten Tomatoes on Shrek: 88%")
