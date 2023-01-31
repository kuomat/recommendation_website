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


# gets the personalized movies list
# personalized_movies = []
# personalized_ids = []
# personalized = None

# redirects to the login page if not logged in
@login_required(login_url='/login/')
def home(response):
    # retreive previous variables from other sessions
    global rated
    if 'rated' in response.session:
        rated = response.session['rated']
    else:
        rated = False

    global personalized_movies, personalized_ids, personalized
    if 'personalized_movies' in response.session:
        personalized_movies = response.session['personalized_movies']
    else:
        personalized_movies = []

    if 'personalized_ids' in response.session:
        personalized_ids = response.session['personalized_ids']
    else:
        personalized_ids = []

    if 'personalized' in response.session:
        personalized = response.session['personalized']
    else:
        personalized = None


    # if haven't rated movies before
    if not rated:
        if response.method == 'POST':
            movie_nums = response.POST.get('movie_nums')
            try:
                int(movie_nums)
                new_path = "/questions/" + movie_nums
                return redirect(new_path)
            except ValueError:
                pass
        return render(response, "main/home.html", {})
    else:
        return render(response, "main/recommendations.html", {"best": best, "personalized": personalized})


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

    # gets the personalized movies list
    global personalized_movies, personalized_ids, personalized
    personalized_movies.extend(movies.get_personalized(answers, indices))
    personalized_ids.extend(movies.get_imdb_id(personalized_movies))
    personalized = {id: movie for id, movie in zip(personalized_ids, personalized_movies)}

    response.session['personalized_movies'] = response.session['personalized_movies'].extend(movies.get_personalized(answers, indices))
    response.session['personalized_ids'] = response.session['personalized_ids'].extend(movies.get_imdb_id(personalized_movies))
    response.session['personalized'] = 
    response.session.modified = True

    return render(response, "main/recommendations.html", {"best": best, "personalized": personalized})

def reset(response):
    global rated
    rated = False
    print("Reset rated")
    return redirect("/home")