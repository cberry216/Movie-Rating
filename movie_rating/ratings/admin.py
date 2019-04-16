from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Group,
    GroupAdminMember,
    Invitation,
    Movie
)

# Register your models here.
admin.site.register(User, UserAdmin)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'created']


@admin.register(GroupAdminMember)
class GroupAdminMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'group']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['invitation_id', 'sender', 'receiver', 'group', 'status']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'added_to_db']
