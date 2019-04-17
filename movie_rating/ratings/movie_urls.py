from django.urls import path

from .views import (
    search_movie
)

urlpatterns = [
    path('rate-movie/', search_movie, name='rate-movie'),
]
