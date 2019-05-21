from django.urls import path

from .views import (
    group,
)

urlpatterns = [
    path('/', group, name='group'),
]
