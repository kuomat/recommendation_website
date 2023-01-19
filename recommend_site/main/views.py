from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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


@login_required(login_url='/login/')
def questions(response, ratings):
    # randomly get the movies and put them in a list
    movies_df = pd.read_csv("main/movies.csv")
    movies = []
    for _ in range(ratings):
        index = random.randint(0, movies_df.shape[0] - 1)
        movies.append(movies_df.loc[index, 'title'])

    return render(response, "main/questions.html", {"movies": movies})