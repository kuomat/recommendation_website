from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RatingQuestionsForm
from . import movies

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
    movie_qs, indices = movies.generate_questions(ratings)
    questions, answers = [], []

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
            indices = ','.join(map(str, indices))
            url = reverse("recommendations", kwargs={"answers": answers, "indices": indices})
            return redirect(url)

    else:
        form = RatingQuestionsForm(questions=questions)

    return render(response, "main/questions.html", {"form": form})

@login_required(login_url='/login/')
def recommendations(response, answers, indices):
    # puts the arrays back
    answers = answers.split(",")
    print(answers)
    print(type(answers[0]))
    indices = indices.split(",")

    # gets the movies with the highest recommendations
    best_movies = movies.get_favorites()

    # gets the personalized movies list
    personalized_movies = movies.get_personalized(answers, indices)
    print(personalized_movies)
    return render(response, "main/recommendations.html", {"best_movies": best_movies, "personalized": personalized_movies})