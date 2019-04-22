from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import homepage, dashboard

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('movie/', include('ratings.movie_urls')),
    path('user/', include('ratings.user_urls')),
]
