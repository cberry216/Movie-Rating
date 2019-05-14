from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from .models import Group, Rating, Movie


def get_item_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def get_item_or_none_from_queryset(query_set, **kwargs):
    try:
        return query_set.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def get_unrated_movies_from_group(user):
    if user.group:
        group = get_item_or_none(Group, group_id=user.group.group_id)
        group_ratings = Rating.objects.filter(user__in=group.users.all())
        group_movies = Movie.objects.filter(movie_id__in=group_ratings.values_list('movie__movie_id'))
        user_movies = Movie.objects.filter(movie_id__in=user.ratings.values_list('movie__movie_id'))
        return [movie for movie in group_movies if movie not in user_movies]
    else:
        return None


def user_has_rated_movie(user, movie):
    user_rating_for_movie = get_item_or_none(Rating, user=user, movie=movie)
    return user_rating_for_movie is not None


def user_has_rated_movie_by_id(user, imdb_id):
    movie = get_item_or_none(Movie, imdb_id=imdb_id)
    if movie:
        return user_has_rated_movie(user, movie)


def movie_in_database(imdb_id):
    movie = get_item_or_none(Movie, imdb_id=imdb_id)
    return movie is not None


def parse_movie_json(omdb_resp):
    # CHAR - NOT NULL - ex. "tt5884052"
    imdb_id = omdb_resp['imdbID']

    # CHAR - NOT NULL - ex. "The Curious Case of Benjamin Button"
    title = omdb_resp['Title']

    # CHAR - NOT NULL - ex. "PG"
    rated = omdb_resp['Rated']

    # DATE - NOT NULL - ex. "09 May 2019"
    released = datetime.strptime(omdb_resp['Released'], "%d %b %Y")

    # INTEGER - NOT NULL - ex. "104 min"
    runtime_minutes = int(omdb_resp['Runtime'].split(' ')[0])

    # CHAR - NULL - ex. "Action, Adventure"
    if omdb_resp['Genre'] != 'N/A':
        genre = omdb_resp['Genre'].split(',')[0]
    else:
        genre = None

    # CHAR - NULL - ex: "David Fincher"
    if omdb_resp['Director'] != 'N/A':
        director = omdb_resp['Director']
    else:
        director = None

    # TEXT - NULL - ex: "Journalist Mikael Blomkvist is aided in his search..."
    if omdb_resp['Plot'] != 'N/A':
        plot = omdb_resp['Plot']
    else:
        plot = None

    # CHAR - NULL - ex: "https://m.media-amazon.com/images/M..."
    if omdb_resp['Poster'] != 'N/A':
        poster_link = omdb_resp['Poster']
    else:
        poster_link = None

    # DECIMAL - NULL - ex: "9.3"
    if omdb_resp['imdbRating']:
        imdb_rating = float(omdb_resp['imdbRating'])
    else:
        imdb_rating = None

    # INTEGER - NULL - ex: "86%"
    if len(omdb_resp['Ratings']) >= 2:
        rt_rating = int(omdb_resp['Ratings'][1]['Value'].split('%')[0])
    else:
        rt_rating = None

    return Movie(
        imdb_id=imdb_id,
        title=title,
        rated=rated,
        released=released,
        runtime_minutes=runtime_minutes,
        genre=genre,
        director=director,
        plot=plot,
        poster_link=poster_link,
        imdb_rating=imdb_rating,
        rt_rating=rt_rating
    )
