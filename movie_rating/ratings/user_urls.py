from django.contrib.auth import views as auth_views
from django.urls import path

from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view, name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view, name='password_change_done'),
]
