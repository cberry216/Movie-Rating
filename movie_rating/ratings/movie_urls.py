from django.urls import path

from .views import (
    search_movie,
    movie_detail,
    rate_movie,
)

urlpatterns = [
    path('rate-movie/', search_movie, name='search_movie'),
    path('rate-movie/<imdb_id>', rate_movie, name='rate_movie'),
    path('<imdb_id>/', movie_detail, name='movie_detail'),
]
