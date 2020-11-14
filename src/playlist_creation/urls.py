from django.urls import path
from . import views

urlpatterns = [
    path('playlist_creation', views.index, name='index'),
]