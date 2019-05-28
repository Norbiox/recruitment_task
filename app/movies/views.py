from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from omdb import OMDBClient
from requests.exceptions import HTTPError

from movies import models


@require_http_methods(["GET", "POST"])
def movies(request):
    if request.method == "GET":
        movies = models.Movie.objects.all()
        return JsonResponse([movie.to_dict() for movie in movies], safe=False)
    elif request.method == "POST":
        title = request.POST.get("title", None)
        if title is None:
            return HttpResponse("'title' was not given", status=400)
        client = OMDBClient(apikey=settings.OMDBAPIKEY)
        try:
            omdb_response = client.get(title=title)
        except HTTPError as e:
            if e.response.status_code == 401:
                return HttpResponse("omdbAPI key is invalid", status=401)
            return e
        if omdb_response == {}:
            return JsonResponse({})
        movie = models.Movie.from_dict(omdb_response)
        movie.save()
        return JsonResponse(movie.to_dict())
