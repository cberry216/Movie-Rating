import requests

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Max, Min, Sum, F
from django.shortcuts import render, redirect

from math import ceil

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
    user_has_rated_movie_by_id,
    movie_in_database,
    parse_movie_json,
)
from .models import (
    Movie,
    Rating,
    Group,
    Rating,
    User,
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
    page = 1
    max_page = 1
    total_results = 0
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            omdb_endpoint = f'http://www.omdbapi.com/?apikey=225ea357&type=movie&s='
            omdb_call = omdb_endpoint + query
            if 'page' in request.GET:
                page = request.GET['page']
                omdb_call += '&page=' + page
            omdb_resp = requests.get(omdb_call)
            omdb_resp = omdb_resp.json()
            if omdb_resp['Response'] == 'True':
                found_results = True
                results = omdb_resp['Search']
                if int(omdb_resp['totalResults']) > 10 * (int(page) + 1):
                    has_next_page = True
                total_results = int(omdb_resp['totalResults'])
                max_page = ceil(total_results / 10)
    return render(request, 'ratings/search_movie.html', {
        'section': 'search',
        'search_form': search_form,
        'query': query,
        'found_results': found_results,
        'results': results,
        'has_next_page': has_next_page,
        'page': page,
        'max_page': max_page,
        'unrated_group_movies': get_unrated_movies_from_group(request.user),
        'total_results': total_results
    })


@login_required
def movie_detail(request, imdb_id):
    group = None
    group_ratings = {}

    if not user_has_rated_movie(request.user, Movie.objects.get(imdb_id=imdb_id)):
        # TODO: Rate movie instead
        pass
    movie_ratings = Rating.objects.filter(movie__imdb_id=imdb_id)
    user_rating = movie_ratings.get(user=request.user).rating

    try:
        group = get_item_or_none(Group, group_id=request.user.group.group_id)
    except AttributeError:
        group = None
    if group is not None:
        group_query = group.users.exclude(user_id=request.user.user_id)
        if len(group_query) > 0:
            for member in group_query:
                rating = get_item_or_none_from_queryset(movie_ratings, user=User.objects.get(username=member))
                group_ratings[member.username] = None if rating is None else rating.rating
    global_rating = float("{0:.1f}".format(movie_ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']))
    movie = Movie.objects.get(imdb_id=imdb_id)
    return render(request, 'ratings/movie_detail.html', {
        'user_rating': user_rating,
        'group': group,
        'group_ratings': group_ratings,
        'global_rating': global_rating,
        'movie': movie
    })


@login_required
def rate_movie(request, imdb_id):
    if user_has_rated_movie_by_id(request.user, imdb_id):
        return redirect('movie_detail', imdb_id=imdb_id)

    if movie_in_database(imdb_id):
        movie = Movie.objects.get(imdb_id=imdb_id)
    else:
        omdb_endpoint = f'http://www.omdbapi.com/?apikey=225ea357&type=movie&i='
        omdb_call = omdb_endpoint + imdb_id
        omdb_resp = requests.get(omdb_call)
        omdb_resp = omdb_resp.json()
        if omdb_resp['Response'] == 'True':
            movie = parse_movie_json(omdb_resp)
            movie.save()

    if request.method == 'POST':
        form = RateMovieForm(request.POST)

        if form.is_valid():
            form.save()
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


def group(request):
    if request.user.group is None:
        has_group = False
        return render(request, 'ratings/group.html', {
            'section': 'group',
            'has_group': has_group
        })

    user_ratings = Rating.objects.filter(user=request.user)
    user_movies = list(map(lambda rating: rating.movie, user_ratings))

    group = request.user.group
    members = group.users.all()
    member_count = len(members)

    group_ratings = Rating.objects.filter(user_id__in=members.values_list('user_id'))
    rated_movies = list(map(lambda rating: rating.movie, group_ratings))

    movie_ratings = dict()

    for movie in rated_movies:
        if movie.title not in movie_ratings:
            movie_ratings[movie.title] = dict()
            if movie in user_movies:
                group_ratings_for_movie = group_ratings.filter(movie=movie)
                movie_ratings[movie.title]['data'] = movie
                movie_ratings[movie.title]['users'] = dict()
                movie_ratings[movie.title]['rating'] = movie.imdb_rating

                # User has rated current movie
                movie_ratings[movie.title]['has_rated'] = True

                # All users have rated current movie
                if len(group_ratings_for_movie) == member_count:
                    movie_ratings[movie.title]['is_complete'] = True
                else:
                    movie_ratings[movie.title]['is_complete'] = False

                # Average rating of current movie
                movie_ratings[movie.title]['avg_rating'] = '{0:.1f}'.format(
                    group_ratings_for_movie.aggregate(avg=Avg('rating'))['avg'])

                # IMDB accuracy of current movie average
                if movie.imdb_id is not None:
                    movie_ratings[movie.title]['imdb_diff'] = '{0:+.1f}'.format(float(
                        movie_ratings[movie.title]['avg_rating']) - float(movie.imdb_rating))

                for member in members:
                    rating = get_item_or_none_from_queryset(group_ratings, user=member, movie=movie)
                    if rating is not None:
                        movie_ratings[movie.title]['users'][member.username] = rating
                    else:
                        movie_ratings[movie.title]['users'][member.username] = None
            else:
                movie_ratings[movie.title]['data'] = movie
                movie_ratings[movie.title]['has_rated'] = False
                movie_ratings[movie.title]['is_complete'] = False
                movie_ratings[movie.title]['avg_rating'] = None
                movie_ratings[movie.title]['imdb_diff'] = None

    return render(request, 'ratings/group.html', {
        'section': 'group',
        'has_group': True,
        'movie_ratings': movie_ratings,
    })
