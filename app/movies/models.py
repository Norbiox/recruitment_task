from django.db import models as m


class Actor(m.Model):
    name = m.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comment(m.Model):
    text = m.CharField(max_length=500)

    def __str__(self):
        return self.text


class Country(m.Model):
    name = m.CharField(max_length=30)

    def __str__(self):
        return self.name


class Director(m.Model):
    name = m.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(m.Model):
    name = m.CharField(max_length=50)

    def __str__(self):
        return self.name


class Language(m.Model):
    name = m.CharField(max_length=30)

    def __str__(self):
        return self.name


class Producer(m.Model):
    name = m.CharField(max_length=100)

    def __str__(self):
        return self.name


class RatingSource(m.Model):
    name = m.CharField(max_length=100)

    def __str__(self):
        return self.name


class Writer(m.Model):
    name = m.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(m.Model):
    actors = m.ManyToManyField(Actor)
    awards = m.CharField(max_length=100)
    box_office = m.IntegerField()
    comments = m.ManyToManyField(Comment)
    countries = m.ManyToManyField(Country)
    directors = m.ManyToManyField(Director)
    dvd = m.DateField()
    genres = m.ManyToManyField(Genre)
    imdb_rating = m.FloatField()
    imdb_id = m.CharField(max_length=20)
    imdb_votes = m.IntegerField()
    languages = m.ManyToManyField(Language)
    metascore = m.IntegerField()
    plot = m.CharField(max_length=500)
    poster = m.URLField(max_length=200)
    production = m.ForeignKey('Producer', related_name='movies',
                              on_delete=m.CASCADE)
    rated = m.CharField(max_length=5)
    released = m.DateField()
    response = m.BooleanField()
    runtime = m.CharField(max_length=10)
    title = m.CharField(max_length=200)
    type = m.CharField(max_length=20)
    website = m.URLField(max_length=200)
    year = m.IntegerField()


class MovieRating(m.Model):
    movie = m.ForeignKey('Movie', related_name='ratings', on_delete=m.CASCADE)
    source = m.ForeignKey('RatingSource', related_name='movies', on_delete=m.CASCADE)
    value = m.CharField(max_length=10)


class MovieWriter(m.Model):
    movie = m.ForeignKey('Movie', related_name='writers', on_delete=m.CASCADE)
    writer = m.ForeignKey('Writer', related_name='movies', on_delete=m.CASCADE)
    notes = m.CharField(max_length=200)
