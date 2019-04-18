from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('movie/', include('ratings.movie_urls')),
    path('user/', include('ratings.user_urls')),
]
