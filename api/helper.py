from django.conf import settings
import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
from movie.models import Movie,Review
from accounts.models import User


def fetch_movie_data(movie_id):
    try:
        response = requests.get(f'{settings.TMDB_API_URL}/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}')
        data = response.json()
        return {
            'title': data['title'],
            'description': data['overview'],
            'release_date': data['release_date'],
            'genre': ', '.join([genre['name'] for genre in data['genres']]),
            'poster': f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        }
    except:
        return False
    
def fetch_now_playing_movies(movie_type):
    try:
        if movie_type=='now_playing':
            url = f"{settings.TMDB_API_URL}/movie/now_playing?language=en-US&page=1"
        elif movie_type=='top_rated':
            url = f"{settings.TMDB_API_URL}/movie/top_rated?language=en-US&page=1"
        elif movie_type=='upcoming':
            url = f"{settings.TMDB_API_URL}/movie/upcoming?language=en-US&page=1"
        else:
            url = f"{settings.TMDB_API_URL}/movie/popular?language=en-US&page=1"

        headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}"  
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(response.json().get('results', [])[0])
            return response.json().get('results', [])
        return []
    except:
        return []
    



def get_user_reviews(user_id):
    reviews = Review.objects.filter(user_id=user_id).select_related('movie')
    return reviews

def get_all_movies():
    movies = Movie.objects.all()
    return movies

def prepare_ratings_matrix(user_reviews, movies):
    num_users = len(set(review.user_id for review in user_reviews))
    num_movies = len(movies)
    ratings_matrix = np.zeros((num_users, num_movies))
   
   
    movie_id_to_index = {movie.id: idx for idx, movie in enumerate(movies)}
    
    for review in user_reviews:
        user_index = num_users - 1  
        movie_index = movie_id_to_index[review.movie_id]
        ratings_matrix[user_index, movie_index] = review.rating
    return ratings_matrix

def calculate_similarity(ratings_matrix):
    similarity_matrix = cosine_similarity(ratings_matrix)
    return similarity_matrix