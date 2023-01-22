from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("questions/<int:ratings>", views.questions, name='questions'),
    path("recommendations/", views.recommendations, name='recommendations'),
    path("test/", views.test, name='test'),
    path("test2/", views.test2, name='test2'),
]