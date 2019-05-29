from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from omdb import OMDBClient
from requests.exceptions import HTTPError

from movies import models, utils


@require_http_methods(["GET", "POST"])
def movies(request):
    if request.method == "GET":
        movies = models.Movie.objects.all()
        return JsonResponse([movie.to_dict() for movie in movies], safe=False)
    elif request.method == "POST":
        title = request.POST.get("title")
        if title is None:
            return HttpResponse("'title' field is required", status=400)
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


@require_http_methods(["GET", "POST"])
def comments(request):
    if request.method == "GET":
        movie_id = request.GET.get("movieID")
        if movie_id is None:
            comments = models.Comment.objects.all()
            return JsonResponse([comment.to_dict() for comment in comments],
                                safe=False)
        movie = get_object_or_404(models.Movie, pk=movie_id)
        comments = models.Comment.objects.filter(movie=movie)
        return JsonResponse([comment.to_dict() for comment in comments],
                            safe=False)
    if request.method == "POST":
        movie_id = request.POST.get("movieID")
        text = request.POST.get("text")
        if movie_id is None or text is None:
            return HttpResponse("'movieID' and 'text' fields are required",
                                status=400)
        movie = get_object_or_404(models.Movie, pk=movie_id)
        comment = models.Comment(movie=movie, text=text)
        comment.save()
        return JsonResponse(comment.to_dict())


@require_http_methods(["GET"])
def top(request):
    date_boundaries = {}
    begin_date = request.GET.get('begin_date')
    end_date = request.GET.get('end_date')
    if begin_date is not None:
        date_boundaries['begin_datetime'] = utils.iso_string_to_date(begin_date)
    if end_date is not None:
        date_boundaries['end_datetime'] = utils.iso_string_to_date(end_date)
    movies = models.Movie.objects.all()
    movies_comments = {
        movie: movie.get_total_comments(**date_boundaries)
        for movie in movies
    }
    ranks = sorted(list(set(movies_comments.values())), reverse=True)
    ranked_movies = []
    for movie, total_comments in movies_comments.items():
        rank = ranks.index(total_comments) + 1
        ranked_movies.append({
            "movie_id": movie.id,
            "total_comments": total_comments,
            "rank": rank
        })
    top = sorted(ranked_movies, key=lambda movie: movie["rank"])
    return JsonResponse(top, safe=False)
