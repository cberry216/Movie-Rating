from django.urls import path

from .views import (
    search_movie,
    movie_detail
)

urlpatterns = [
    path('rate-movie/', search_movie, name='rate-movie'),
    path('<imdb_id>/', movie_detail, name='movie_detail'),
]
