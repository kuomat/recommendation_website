from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("questions/<int:ratings>", views.questions, name='questions'),
    path("recommendations/<str:answers>", views.recommendations, name='recommendations'),
]