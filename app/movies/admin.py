from django.contrib import admin

from .models import (
    Actor,
    Comment,
    Country,
    Director,
    Genre,
    Producer,
    RatingSource,
    Writer,
    Movie,
    MovieRating,
    MovieWriter
)


admin.site.register(Actor)
admin.site.register(Comment)
admin.site.register(Country)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Producer)
admin.site.register(RatingSource)
admin.site.register(Writer)
admin.site.register(Movie)
admin.site.register(MovieRating)
admin.site.register(MovieWriter)
