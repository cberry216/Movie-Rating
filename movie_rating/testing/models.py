from django.db import models

# Create your models here.


class Group(models.Model):
    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=120)
    group_id = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='users',
        null=True
    )
    invitation_count = models.IntegerField(default=0)


class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60)
    rated = models.CharField(max_length=10)
    released = models.DateField()
    runtime_minutes = models.IntegerField()
    genre = models.CharField(max_length=40, null=True, blank=True)
    director = models.CharField(max_length=100, null=True, blank=True)
    plot = models.TextField(null=True)
    poster_link = models.CharField(max_length=200, null=True)
    imdb_rating = models.FloatField(null=True)
    rt_rating = models.IntegerField(null=True)
    added_to_db = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    rating_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    movie_id = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.FloatField()
    comment = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
