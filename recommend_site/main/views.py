from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import movies
import random
import pandas as pd

# redirects to the login page if not logged in
@login_required(login_url='/login/')
def home(response):
    if response.method == 'POST':
        movie_nums = response.POST.get('movie_nums')
        try:
            int(movie_nums)
            new_path = "/questions/" + movie_nums
            return redirect(new_path)
        except ValueError:
            pass
    return render(response, "main/home.html", {})


# randomly chooses movies and put them into a questionaire
@login_required(login_url='/login/')
def questions(response, ratings):
    # stores the movies into movie_qs
    movies_df = pd.read_csv("main/movies.csv")
    movie_qs = []
    for _ in range(ratings):
        index = random.randint(0, movies_df.shape[0] - 1)
        movie_qs.append(movies.fix_movie(movies_df.loc[index, 'title']))

    if response.method == 'POST':
        movie_scores = response.POST.get('rate_movies')
        return render(response, "main/test.html", {"scores": movie_scores})

    return render(response, "main/questions.html", {"movies": movie_qs})

@login_required(login_url='/login/')
def recommendations(response):
    # gets the movies with the highest recommendations
    best_movies = movies.get_favorites()
    return render(response, "main/recommendations.html", {"best_movies": best_movies})