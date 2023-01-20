import pandas as pd
import numpy as np

NUM_FAVORITES = 10

movies_df = pd.read_csv("main/movies.csv")
ratings_df = pd.read_csv("main/ratings.csv")

def fix_movie(movie):
    l = movie.split(",")
    if len(l) == 1:
        return movie
    if len(l) == 2:
        return "The " + l[0] + " " + l[1][5:]
    else:
        return movie

id_to_title = {}
for row in movies_df.itertuples():
    id_to_title[int(row[1])] = fix_movie(row[2])

# gets the movie indices in terms of ratings in ascending order
def get_favorites():
    count = ratings_df.groupby('movieId')['userId'].nunique().reset_index(name="count")
    avg = ratings_df.groupby('movieId')['rating'].mean().reset_index(name="avg_rating")
    ratings = pd.merge(count, avg, on='movieId')

    # remove the rows with less than 15 ratings
    ratings = ratings[ratings['count'] > 100]

    ratings_np = ratings['avg_rating'].to_numpy()
    indices = np.argpartition(ratings_np, -10)[-10:]
    indices = indices[np.argsort(ratings_np[indices])] # mean ratings in ascending order
    top_movies_id = [ratings.iloc[index]['movieId'] for index in indices]

    top_movies_names = [id_to_title[movie_id] for movie_id in top_movies_id]
    return top_movies_names
