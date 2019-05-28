from django.contrib import admin

from .models import (
    Comment,
    Movie,
    MovieRating,
)


admin.site.register(Comment)
admin.site.register(Movie)
admin.site.register(MovieRating)
