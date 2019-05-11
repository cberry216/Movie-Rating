import requests

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Max, Min, Sum
from django.shortcuts import render, redirect

from .forms import (
    SearchForm,
    UserRegistrationForm,
    RateMovieForm
)
from .helpers import (
    get_item_or_none,
    get_item_or_none_from_queryset,
    get_unrated_movies_from_group,
    user_has_rated_movie,
)
from .models import (
    Movie,
    Rating,
    Group,
    Rating,
)

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
    total_results = 0
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            omdb_endpoint = f'http://www.omdbapi.com/?apikey=225ea357&type=movie&s='
            omdb_call = omdb_endpoint + query
            omdb_resp = requests.get(omdb_call)
            omdb_resp = omdb_resp.json()
            if omdb_resp['Response'] == 'True':
                found_results = True
                results = omdb_resp['Search']
                if int(omdb_resp['totalResults']) > 10:
                    has_next_page = True
                total_results = omdb_resp['totalResults']
    return render(request, 'ratings/search_movie.html', {
        'section': 'search',
        'search_form': search_form,
        'query': query,
        'found_results': found_results,
        'results': results,
        'has_next_page': has_next_page,
        'unrated_group_movies': get_unrated_movies_from_group(request.user)
    })


@login_required
def movie_detail(request, imdb_id):
    group_members = []
    group_ratings = {}

    if not user_has_rated_movie(request.user, Movie.objects.get(imdb_id=imdb_id)):
        # TODO: Rate movie instead
        pass
    movie_ratings = Rating.objects.filter(movie__imdb_id=imdb_id)
    user_rating = movie_ratings.get(user=request.user).rating

    group = get_item_or_none(Group, group_id=request.user.group.group_id)
    if group is not None:
        group_query = group.users.exclude(user_id=request.user.user_id)
        if len(group_query) > 0:
            for member in group_query:
                group_members.append(member.username)
                rating = get_item_or_none_from_queryset(movie_ratings, user=request.user)
                group_ratings[member.username] = None if rating is None else rating.rating
    global_rating = movie_ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
    movie = Movie.objects.get(imdb_id=imdb_id)
    return render(request, 'ratings/movie_detail.html', {
        'user_rating': user_rating,
        'group_members': group_members,
        'group_ratings': group_ratings,
        'global_rating': global_rating,
        'movie': movie
    })


@login_required
def rate_movie(request, imdb_id):
    if user_has_rated_movie(request.user, Movie.objects.get(imdb_id=imdb_id)):
        return redirect('movie_detail', imdb_id=imdb_id)

    movie = Movie.objects.get(imdb_id=imdb_id)

    if request.method == 'POST':
        form = RateMovieForm(request.POST)

        if form.is_valid():
            form.save()
            # return render(request, 'ratings/rate_movie_success.html')
            return redirect('movie_detail', imdb_id=imdb_id)
    else:
        form = RateMovieForm(initial={'movie': movie, 'user': request.user})
        return render(request, 'ratings/rate_movie.html', {
            'form': form,
            'movie': movie
        })


@login_required
def dashboard(request):
    movies_seen_by_user = Movie.objects.filter(movie_id__in=request.user.ratings.values_list('movie__movie_id'))
    user_ratings = Rating.objects.filter(user=request.user)

    try:
        group = get_item_or_none(Group, group_id=request.user.group.group_id)
    except AttributeError:
        group = None

    movies_seen_by_others = []
    has_group = False
    if group is not None:
        has_group = True
        movies_seen_by_others = Movie.objects.filter(
            movie_id__in=Rating.objects
            .filter(user__in=group.users.all())
            .exclude(user_id=request.user.user_id)
            .values_list('movie__movie_id'))

    return render(request, 'ratings/dashboard.html', {
        'section': 'dashboard',
        'has_group': has_group,
        'movies_seen_by_user': movies_seen_by_user,
        'movies_seen_by_others': movies_seen_by_others,
        'movies_seen_by_both': [movie for movie in movies_seen_by_others if movie in movies_seen_by_user],
        'movies_not_seen_by_user': [movie for movie in movies_seen_by_others if movie not in movies_seen_by_user],
    })
