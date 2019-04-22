from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=60, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    email = models.CharField(max_length=120)
    group = models.ForeignKey(
        Group,
        related_name='users',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


class GroupAdminMember(models.Model):
    group_admin_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class Invitation(models.Model):
    INVITATION_OPTIONS = [
        ('sent', 'sent'),
        ('ignored', 'ignored')
    ]
    invitation_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(
        User,
        related_name='sent_invitations',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_invitations',
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        related_name='invitations_to_join',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=8,
        choices=INVITATION_OPTIONS,
        default='sent'
    )
    sent = models.DateTimeField(auto_now_add=True)


class Movie(models.Model):
    MOVIE_RATINGS = [
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
    ]
    movie_id = models.AutoField(primary_key=True)
    imdb_id = models.CharField(max_length=12)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    rated = models.CharField(
        max_length=5,
        choices=MOVIE_RATINGS,
        default='PG-13',
        null=True,
        blank=True
    )
    released = models.DateField()
    runtime_minutes = models.IntegerField()
    genre = models.CharField(max_length=20, null=True, blank=True)
    director = models.CharField(max_length=80, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    poster_link = models.CharField(max_length=250, null=True, blank=True)
    imdb_rating = models.FloatField(null=True, blank=True)
    rt_rating = models.IntegerField(null=True, blank=True)
    added_to_db = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        related_name='ratings',
        on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie,
        related_name='ratings',
        on_delete=models.CASCADE
    )
    rating = models.FloatField()
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
