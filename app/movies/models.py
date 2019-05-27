from django.db import models as m


class Actor(m.Model):
    name = m.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    box_office = m.CharField(max_length=20)
    countries = m.ManyToManyField(Country)
    directors = m.ManyToManyField(Director)
    dvd = m.DateField()
    genres = m.ManyToManyField(Genre)
    imdb_rating = m.FloatField()
    imdb_id = m.CharField(max_length=20)
    imdb_votes = m.CharField(max_length=10)
    languages = m.ManyToManyField(Language)
    metascore = m.IntegerField()
    plot = m.CharField(max_length=500)
    poster = m.URLField(max_length=200, blank=True, null=True)
    production = m.ForeignKey('Producer', related_name='movies',
                              on_delete=m.CASCADE)
    rated = m.CharField(max_length=5)
    released = m.DateField()
    response = m.CharField(max_length=5)
    runtime = m.CharField(max_length=10)
    title = m.CharField(max_length=200)
    type = m.CharField(max_length=20)
    website = m.URLField(max_length=200, blank=True, null=True)
    year = m.IntegerField()

    def __str__(self):
        return self.title


class Comment(m.Model):
    movie = m.ForeignKey('Movie', related_name='comments', on_delete=m.CASCADE)
    text = m.CharField(max_length=500)
    created = m.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class MovieRating(m.Model):
    movie = m.ForeignKey('Movie', related_name='ratings', on_delete=m.CASCADE)
    source = m.ForeignKey('RatingSource', related_name='movies',
                          on_delete=m.CASCADE)
    value = m.CharField(max_length=10)

    def __str__(self):
        return f"{self.source} on {self.movie}: {self.value}"


class MovieWriter(m.Model):
    movie = m.ForeignKey('Movie', related_name='writers', on_delete=m.CASCADE)
    writer = m.ForeignKey('Writer', related_name='movies', on_delete=m.CASCADE)
    notes = m.CharField(max_length=200)

    def __str__(self):
        return f"{self.writer} ({self.notes})"
