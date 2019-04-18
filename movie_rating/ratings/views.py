import requests

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from .forms import SearchForm, UserRegistrationForm
from .helpers import (
    get_unrated_movies_from_group,
    user_has_rated_movie,
)
from .models import Movie

# Create your views here.


def homepage(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def search_movie(request):
    search_form = SearchForm()
    query = None
    found_results = False
    results = []
    has_next_page = False
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            omdb_endpoint = f'http://www.omdbapi.com/?apikey=225ea357&type=movie&s='
            omdb_call = omdb_endpoint + query
            omdb_resp = requests.get(omdb_endpoint + query)
            omdb_resp = omdb_resp.json()
            if omdb_resp['Response'] == 'True':
                found_results = True
                results = omdb_resp['Search']
                if int(omdb_resp['totalResults']) > 10:
                    has_next_page = True
    return render(request, 'ratings/search_movie.html', {
        'search_form': search_form,
        'query': query,
        'found_results': found_results,
        'results': results,
        'has_next_page': has_next_page,
        'unrated_group_movies': get_unrated_movies_from_group(request.user)
    })


@login_required
def rate_movie(request, imdb_id):
    if user_has_rated_movie(request.user, Movie.objects.get(imdb_id=imdb_id)):
        pass
