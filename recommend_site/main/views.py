from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote_plus, quote_plus
from django.urls import reverse
from .forms import RatingQuestionsForm
from . import movies

# gets the highest recommendations of all movies
best_movies = movies.get_favorites()
best_ids = movies.get_imdb_id(best_movies)
best = {id: movie for id, movie in zip(best_ids, best_movies)}

# redirects to the login page if not logged in
@login_required(login_url='/login/')
def home(response):
    # retreive previous variables from other sessions
    if 'rated' not in response.session:
        response.session['rated'] = False

    if 'personalized' not in response.session:
        response.session['personalized'] = []

    if 'answers' not in response.session:
        response.session['answers'] = []

    if 'indices' not in response.session:
        response.session['indices'] = []

    response.session.modified = True

    # if haven't rated movies before
    if not response.session['rated']:
        # go to select the number of ratings to give
        return redirect(select_questions)
    else:
        # show the recommendations
        return render(response, "main/recommendations.html", {"best": best, "personalized": response.session['personalized']})

@login_required(login_url='/login/')
def select_questions(response):
    if response.method == 'POST':
        movie_nums = response.POST.get('movie_nums')
        try:
            int(movie_nums)
            new_path = "/questions/" + movie_nums
            return redirect(new_path)
        except ValueError:
            pass

    return render(response, "main/select_questions.html", {})

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
        response.session['rated'] = True
        response.session.modified = True

        form = RatingQuestionsForm(response.POST, questions=questions)
        if form.is_valid():
            for i in range(len(questions)):
                answers.append(form.cleaned_data[f"question_{i+1}"])

            # converts array into a string to be passed into url
            answers = quote_plus(','.join(map(str, answers)))
            indices = quote_plus(','.join(map(str, indices)))

            url = reverse("recommendations", kwargs={"answers": answers, "indices": indices})
            return redirect(url)

    else:
        form = RatingQuestionsForm(questions=questions)

    return render(response, "main/questions.html", {"form": form})

@login_required(login_url='/login/')
def recommendations(response, answers, indices):
    # puts the arrays back
    answers = unquote_plus(answers).split(",")
    indices = unquote_plus(indices).split(",")

    response.session['answers'].extend(answers)
    response.session['indices'].extend(indices)

    # gets the personalized movies list
    personalized_movies = movies.get_personalized(response.session['answers'], response.session['indices'] )
    personalized_ids = movies.get_imdb_id(personalized_movies)

    response.session['personalized'] = {id: movie for id, movie in zip(personalized_ids, personalized_movies)}
    response.session.modified = True

    return render(response, "main/recommendations.html", {"best": best, "personalized": response.session['personalized']})

def reset(response):
    response.session['rated'] = False
    response.session['answers'] = []
    response.session['indices'] = []
    response.session['personalized'] = []
    response.session.modified = True
    return redirect("/home")