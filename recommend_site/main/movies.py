import pandas as pd
import numpy as np
import random
from numpy.linalg import norm
from imdb import IMDb


TOP_FAVS = 10
TOP_USERS = 15
imdb = IMDb()

movies_df = pd.read_csv("movies.csv")
ratings_df = pd.read_csv("ratings.csv")

# fixes the movie names
def fix_movie(movie):
    l = movie.split(",")
    if len(l) == 1:
        return movie
    elif len(l) == 2:
        return "The " + l[0] + " " + l[1][5:]
    else:
        return movie

def data_handling():
    # change the movie's id to the title of the movie
    id_to_title = {}
    for row in movies_df.itertuples():
        id_to_title[int(row[1])] = fix_movie(row[2])

    # change the movie's id to index in matrix
    movie_id_to_index = {}
    index = 0
    for row in movies_df['movieId']:
        movie_id_to_index[row] = index
        index += 1

    # number of unique users and movies
    num_users = ratings_df['userId'].nunique()
    num_movies = movies_df['movieId'].nunique()

    # creates a matrix of users by movies
    data_mat = np.zeros((num_users, num_movies))

    for row in ratings_df.itertuples():
        data_mat[row[1] - 1, movie_id_to_index[row[2]]] = row[3]

    return id_to_title, movie_id_to_index, data_mat, num_movies


id_to_title, movie_id_to_index, data_mat, num_movies = data_handling()

# generate the questions to ask
def generate_questions(num):
    # TODO: CHANGE THIS SO THAT IF IT GENREATES A QUESTION ALREADY WATCHED, WILL GENERATE AGAIN
    number_list = list(range(0, movies_df.shape[0]))
    indices = random.sample(number_list, num)
    movies = [fix_movie(movies_df.loc[index, 'title']) for index in indices]
    return movies, indices


# gets the movie indices in terms of ratings in ascending order
def get_favorites():
    count = ratings_df.groupby('movieId')['userId'].nunique().reset_index(name="count")
    avg = ratings_df.groupby('movieId')['rating'].mean().reset_index(name="avg_rating")
    ratings = pd.merge(count, avg, on='movieId')

    # remove the rows with less than 15 ratings
    ratings = ratings[ratings['count'] > 100]

    ratings_np = ratings['avg_rating'].to_numpy()
    indices = np.argpartition(ratings_np, -TOP_FAVS)[-TOP_FAVS:]
    indices = indices[np.argsort(ratings_np[indices])] # mean ratings in ascending order
    top_movies_id = [ratings.iloc[index]['movieId'] for index in indices]

    top_movies_names = [id_to_title[movie_id] for movie_id in top_movies_id]
    return top_movies_names

# finds top similar users
def top_similars(user_vector):
    cosine_mat = np.zeros(len(data_mat))

    for index, row in enumerate(data_mat):
        cosine = np.dot(user_vector, row) / (norm(user_vector) * norm(row))
        cosine_mat[index] = cosine

    top_indices = np.argpartition(cosine_mat, -TOP_USERS)[-TOP_USERS:]
    top_dists = [cosine_mat[index] for index in top_indices]
    return top_indices, top_dists

# predicts a user's rating for all movies
def predict_movie(user_vector, watched):
    top_indices, top_dists = top_similars(user_vector)
    res = []

    for movie_id in movie_id_to_index.keys():
        # if haven't watched
        if watched[movie_id_to_index[movie_id]] == 0:
            total_ratings = 0

            # adds all the ratings given by the similar users for each movie
            for i in range(len(top_indices)):
                total_ratings += (data_mat[top_indices[i], movie_id_to_index[movie_id]] * top_dists[i])
            res.append(total_ratings / np.sum(top_dists))
        else:
            # predicts the movie to be 0 so it doesn't affect the personalized movie list
            res.append(0)

    return res

# converts the user's answers to a user vector
def convert_ans_to_user_vector(answers, indices):
    # TODO: CHANGE THIS SO THAT IT WILL REMEMBER WHAT HAPPENED BEFORE
    user_vector = np.zeros(num_movies)

    # an array to store if the user already watched certain movies
    # TODO: CHANGE THIS SO THAT IT WILL REMEMBER WHAT HAPPENED BEFORE
    watched = np.zeros(num_movies)

    for i in range(len(indices)):
        index = int(indices[i])
        try:
            # gives the movie of the user vector a rating
            user_vector[index] = int(answers[i])

            # changes the value at the movie's index to 1 if already watched
            watched[index] = 1
        except ValueError:
            # gives the movie a rating of 0 if haven't watched
            pass

    return user_vector, watched

# gets personalized movie recommendations based on the user's answers
def get_personalized(answers, indices):
    user_vector, watched = convert_ans_to_user_vector(answers, indices)

    # gets all the predicted values from the user's answers
    predictions = predict_movie(user_vector, watched)

    # gives everyone's favorites if no ratings
    if sum(watched) == 0:
        return get_favorites()

    # gets the indices of the best personalized movie list
    best_movies_indices = np.argpartition(predictions, -TOP_FAVS)[-TOP_FAVS:]

    # gets the movies' names from the indices
    movie_names = [fix_movie(movies_df.loc[index, 'title']) for index in best_movies_indices]
    return movie_names

# gets the imdb-id of the movies
def get_imdb_id(movies):
    res = []

    # search the imdb library
    for movie in movies:
        movie_name = movie.split('(')[0]
        results = imdb.search_movie(movie_name)
        res.append(results[0].movieID)

    return res

def search_movies(movie_name):
    movies = imdb.search_movie(movie_name)[:3]
    # indices = [get_movie_index(movie) for movie in movies]
    # return movies, indices
    return movies

# def get_movie_index(movie):
    # find the movie id
    # use movie_id_to_index to get index