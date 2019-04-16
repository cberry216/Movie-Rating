from django.db import models

from movie_rating.user.models import User

# Create your models here.


class Group(models.Model):
    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=60, unique=True)
    created = models.DateTimeField(auto_now_add=True)


class GroupAdmin(models.Model):
    GROUP_ADMIN_CHOICES = [
        ('active', 'active'),
        ('inactive', 'inactive')
    ]

    group_admin_id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=8,
        choices=GROUP_ADMIN_CHOICES,
        default='active'
    )


class Invitation(models.Model):
    INVITATION_OPTIONS = [
        ('sent', 'sent'),
        ('ignored', 'ignored')
    ]
    invitation_id = models.IntegerField(primary_key=True)
    sender = models.ForeignKey(
        User,
        related_name='sent_invitations'
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_invitations',
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        related_name='invitations_to_join'
    )
    status = models.CharField(
        max_length=8,
        choices=INVITATION_OPTIONS,
        default='sent'
    )
    sent = models.DateTimeField(auto_now_add=True)
