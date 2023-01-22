from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    # stores the movies into movie_qs
    movies_df = pd.read_csv("main/movies.csv")
    movie_qs = []
    for _ in range(ratings):
        index = random.randint(0, movies_df.shape[0] - 1)
        movie_qs.append(movies.fix_movie(movies_df.loc[index, 'title']))

    # submitting the questions
    if response.method == 'POST':
        movie_scores = response.POST.get('rating1')
        movie_2 = response.POST.get('rating2')
        print("movie scores:", movie_scores, movie_2)
        return render(response, "main/test.html", {"scores": movie_scores})

    return render(response, "main/questions.html", {"movies": movie_qs})

@login_required(login_url='/login/')
def recommendations(response):
    # gets the movies with the highest recommendations
    best_movies = movies.get_favorites()
    return render(response, "main/recommendations.html", {"best_movies": best_movies})

def test(response):
    movies_df = pd.read_csv("main/movies.csv")
    movie_qs = []
    for _ in range(5):
        index = random.randint(0, movies_df.shape[0] - 1)
        movie_qs.append(movies.fix_movie(movies_df.loc[index, 'title']))

    questions = []
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
            # text = form.fields
            # text = form.cleaned_data['question_5']
            # print("nice")
            # for ele in form:
            #     print(ele)
            print("nice")
            # movie_scores = form.cleaned_data['question_3']
            # print(movie_scores)
            # return render(response, "main/test2.html", {"scores": movie_scores})
    else:
        print("illegal")
        form = RatingQuestionsForm(questions=questions)

    for q in form:
        print(q)
    return render(response, "main/test.html", {"movie": movie_qs, "form": form})

def test2(response):
    return render(response, "main/test2.html", {})
