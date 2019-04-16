from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    email = models.CharField(max_length=120)

    def __str__(self):
        return self.username


class Group(models.Model):
    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=60, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class GroupAdminMember(models.Model):
    group_admin_id = models.IntegerField(primary_key=True)
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
    invitation_id = models.IntegerField(primary_key=True)
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
