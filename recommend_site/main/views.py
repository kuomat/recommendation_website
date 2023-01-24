from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RatingQuestionsForm
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
    movies_df = pd.read_csv("main/movies.csv")
    movie_qs, questions, answers = [], [], []
    for _ in range(ratings):
        index = random.randint(0, movies_df.shape[0] - 1)
        movie_qs.append(movies.fix_movie(movies_df.loc[index, 'title']))

    for movie in movie_qs:
        questions.append({'text': movie, 'options': [('not_watched', 'Not Watched'),
                                                     ('1', '1'),
                                                     ('2', '2'),
                                                     ('3', '3'),
                                                     ('4', '4'),
                                                     ('5', '5')]})

    if response.method == 'POST':
        form = RatingQuestionsForm(response.POST, questions=questions)
        if form.is_valid():
            for i in range(len(questions)):
                answers.append(form.cleaned_data[f"question_{i+1}"])

            # converts array into a string to be passed into url
            answers = ','.join(map(str, answers))
            url = reverse("recommendations", kwargs={"answers": answers})
            return redirect(url)

    else:
        form = RatingQuestionsForm(questions=questions)

    return render(response, "main/questions.html", {"form": form})

@login_required(login_url='/login/')
def recommendations(response, answers):
    # puts the array back
    answers = answers.split(",")
    
    # gets the movies with the highest recommendations
    best_movies = movies.get_favorites()
    return render(response, "main/recommendations.html", {"best_movies": best_movies, "answers": answers})