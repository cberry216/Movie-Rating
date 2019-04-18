from django.core.exceptions import ObjectDoesNotExist

from .models import Group, Rating, Movie


def get_item_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
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
