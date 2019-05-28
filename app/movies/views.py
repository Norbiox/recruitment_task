from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods

from movies import models


@require_http_methods(["GET"])
def movies_list(request):
    movies = models.Movie.objects.all()
    return JsonResponse([movie.to_dict() for movie in movies], safe=False)
