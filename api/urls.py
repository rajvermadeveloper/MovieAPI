from django.urls import path,include
from .views import *
urlpatterns = [
    path('user/signup/', UserSignup.as_view(),name="signup"),
    path('user/signin/', UserSignIn.as_view(),name="signin"),
    path('user/profile/', UserProfile.as_view(),name="profile"),
    path('movies/<str:movie_type>', FetchAndStoreMovies.as_view(), name='fetch_and_store_movie'),
    path('movies/', MovieList.as_view(),name="movie"),
    path('search-movie/', SearchMovie.as_view(), name='search_movie'),
    path('recommend-movies/', RecommendMovies.as_view(), name='recommend_movies'),
    path('review/', MovieReview.as_view(), name='review'),
    path('search-review/', SearchReview.as_view(), name='search_review'),
]