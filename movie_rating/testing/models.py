from django.db import models

# Create your models here.


class Group(models.Model):
    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=60)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=60)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='users',
        null=True
    )


class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60)
    genre = models.CharField(max_length=40, null=True, blank=True)
    imdb_rating = models.FloatField(null=True)
    rt_rating = models.IntegerField(null=True)


class Rating(models.Model):
    rating_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.FloatField()
