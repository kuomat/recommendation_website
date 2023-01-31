from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("questions/<str:movie_qs>/<str:indices>", views.questions, name='questions'),
    path("recommendations/<str:answers>/<str:indices>", views.recommendations, name='recommendations'),
    path("reset", views.reset, name='reset'),
    path("select_questions/", views.select_questions, name='select_questions'),
]