from django.db import models as m

from .utils import date_to_string, string_to_date


class Comment(m.Model):
    movie = m.ForeignKey('Movie', related_name='comments', on_delete=m.CASCADE)
    text = m.CharField(max_length=500)
    created = m.DateTimeField(auto_now=True)

    @classmethod
    def from_dict(cls, data):
        movie = Movie.objects.get(pk=data["movieID"])
        return cls.objects.create(movie=movie, text=data["text"])

    def to_dict(self):
        return {
            "ID": self.id,
            "Movie": str(self.movie),
            "Text": self.text,
            "Created": str(self.created)
        }

    def __str__(self):
        return self.text


class MovieRating(m.Model):
    movie = m.ForeignKey('Movie', related_name='ratings', on_delete=m.CASCADE)
    source = m.CharField(max_length=100)
    value = m.CharField(max_length=10)

    @classmethod
    def from_dict(cls, data):
        movie = Movie.objects.get(pk=data["movieID"])
        return cls.objects.create(movie=movie, source=data["Source"],
                                  value=data["Value"])

    def to_dict(self, short=False):
        data = {
            "Source": self.source,
            "Value": self.value
        }
        if not short:
            data["ID"] = self.id
            data["Movie"] = str(self.movie)
        return data

    def __str__(self):
        return f"{self.source} on {self.movie}: {self.value}"


class Movie(m.Model):
    actors = m.CharField(max_length=200, blank=True, null=True)
    awards = m.CharField(max_length=100, blank=True, null=True)
    box_office = m.CharField(max_length=20, blank=True, null=True)
    countries = m.CharField(max_length=100, blank=True, null=True)
    directors = m.CharField(max_length=100, blank=True, null=True)
    dvd = m.DateField(blank=True, null=True)
    genres = m.CharField(max_length=100, blank=True, null=True)
    imdb_rating = m.FloatField(blank=True, null=True)
    imdb_id = m.CharField(max_length=20, unique=True)
    imdb_votes = m.CharField(max_length=10, blank=True, null=True)
    languages = m.CharField(max_length=100, blank=True, null=True)
    metascore = m.IntegerField(blank=True, null=True)
    plot = m.CharField(max_length=500, blank=True, null=True)
    poster = m.URLField(max_length=200, blank=True, null=True)
    production = m.CharField(max_length=100, blank=True, null=True)
    rated = m.CharField(max_length=5, blank=True, null=True)
    released = m.DateField(blank=True, null=True)
    response = m.CharField(max_length=5)
    runtime = m.CharField(max_length=10, blank=True, null=True)
    title = m.CharField(max_length=200)
    type = m.CharField(max_length=20, blank=True, null=True)
    website = m.URLField(max_length=200, blank=True, null=True)
    writers = m.CharField(max_length=300, blank=True, null=True)
    year = m.IntegerField(blank=True, null=True)

    @property
    def total_comments(self):
        return len(Comment.objects.filter(movie=self).all())

    @classmethod
    def capitalize_omdb_entry(cls, omdb_entry):
        new_entry = {}
        for key, value in omdb_entry.items():
            new_entry[key.capitalize()] = value
        new_entry["imdbRating"] = omdb_entry["imdb_rating"]
        new_entry["imdbVotes"] = omdb_entry["imdb_votes"]
        new_entry["imdbID"] = omdb_entry["imdb_id"]
        new_entry["DVD"] = omdb_entry["dvd"]
        new_entry["BoxOffice"] = omdb_entry["box_office"]
        new_entry["Ratings"] = []
        for rating in omdb_entry["ratings"]:
            for key, value in rating.items():
                new_entry[key.capitalize()] = value
        return new_entry

    @classmethod
    def from_dict(cls, data):
        if "title" in data.keys():
            data = cls.capitalize_omdb_entry(data)
        na_keys = [key for key, value in data.items() if value == "N/A"]
        for key in na_keys:
            del data[key]
        imdb_rating = data.get("imdbRating", None)
        metascore = data.get("Metascore", None)
        year = data.get("Year", None)
        new_movie = cls.objects.create(
            actors=data.get("Actors", None),
            awards=data.get("Awards", None),
            box_office=data.get("BoxOffice", None),
            countries=data.get("Country", None),
            directors=data.get("Director", None),
            dvd=string_to_date(data.get("DVD", None)),
            genres=data.get("Genre", None),
            imdb_rating=float(imdb_rating)
            if imdb_rating is not None else None,
            imdb_id=data.get("imdbID"),
            imdb_votes=data.get("imdbVotes", None),
            languages=data.get("Language", None),
            metascore=int(metascore) if metascore is not None else None,
            plot=data.get("Plot", None),
            poster=data.get("Poster", None),
            production=data.get("Production", None),
            rated=data.get("Rated", None),
            released=string_to_date(data.get("Released", None)),
            response=data.get("Response"),
            runtime=data.get("Runtime", None),
            title=data.get("Title"),
            type=data.get("Type", None),
            website=data.get("Website", None),
            writers=data.get("Writer", None),
            year=int(year) if year is not None else None,
        )
        ratings = []
        for rating_dict in data["Ratings"]:
            rating_dict["movieID"] = new_movie.id
            ratings.append(MovieRating.from_dict(rating_dict))
        new_movie._ratings = ratings
        return new_movie

    def save(self, *args, **kwargs):
        if hasattr(self, '_ratings'):
            for rating in self._ratings:
                rating.save()
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "ID": self.id,
            "Title": self.title,
            "Year": self.year or "N/A",
            "Rated": self.rated or "N/A",
            "Released": date_to_string(self.released)
            if self.released is not None else "N/A",
            "Runtime": self.runtime or "N/A",
            "Genre": self.genres or "N/A",
            "Director": self.directors or "N/A",
            "Writer": self.writers or "N/A",
            "Actors": self.actors or "N/A",
            "Plot": self.plot or "N/A",
            "Language": self.languages or "N/A",
            "Country": self.countries or "N/A",
            "Awards": self.awards or "N/A",
            "Poster": self.poster or "N/A",
            "Ratings": [r.to_dict(short=True) for r in self.ratings.all()],
            "Metascore": self.metascore or "N/A",
            "imdbRating": self.imdb_rating or "N/A",
            "imdbVotes": self.imdb_votes or "N/A",
            "imdbID": self.imdb_id or "N/A",
            "Type": self.type or "N/A",
            "DVD": date_to_string(self.dvd) if self.dvd is not None else "N/A",
            "BoxOffice": self.box_office or "N/A",
            "Production": self.production or "N/A",
            "Website": self.website or "N/A",
            "Response": self.response or "N/A"
        }

    def __str__(self):
        return self.title
