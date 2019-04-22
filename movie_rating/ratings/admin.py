from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Group,
    GroupAdminMember,
    Invitation,
    Movie,
    Rating,
)

# Register your models here.
admin.site.register(User, UserAdmin)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'group_name', 'created']


@admin.register(GroupAdminMember)
class GroupAdminMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'user', 'group']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['invitation_id', 'sender', 'receiver', 'group', 'status']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'title', 'genre', 'added_to_db']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rating_id', 'movie', 'user', 'rating', 'comment', 'timestamp']
