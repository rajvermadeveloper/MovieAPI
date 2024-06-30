from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from accounts.serializers import *
from movie.serializers import *
from django.conf import settings
from accounts.renderers import UserRenderers
from django.db.models import Q
from .helper import *
import requests

# ============= CONFIG PART ==============

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomPagination(PageNumberPagination):
    page_size = 10

# =============== USER API ====================

class UserSignup(APIView):
    ''' User Signup by using email,name,password,password2 and tc(Terms & Conditions)'''
    renderer_classes=[UserRenderers]
    def post(self,request,format=None):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successfull!'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserSignIn(APIView):
    ''' User SignIn by using Email and Password '''
    renderer_classes=[UserRenderers]
    def post(self,request,format=None):
        serializer=UserSigninSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Successfully!'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':'Email and Password is not valid!'}},
                status=status.HTTP_404_NOT_FOUND
                )
            
class UserProfile(APIView):
    ''' User SignIn by using Email and Password '''
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        if serializer.data:
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Blacklist the access token
            auth = JWTAuthentication()
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                user, token = user_auth_tuple
            BlacklistedAccessToken.objects.create(token=str(token))

            return Response({"msg": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"error": "Token is blacklisted or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)       

# ============= MOVIE API ============
class FetchAndStoreMovieData(APIView):
    """ Fetch Movie Information by Movie_id  From TMDB API and Store into our Database"""
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self, request, movie_id):
        movie_data = fetch_movie_data(movie_id)
        if movie_data:
            movie, created = Movie.objects.get_or_create(
                user=request.user,
                movie_id=movie_id,
                defaults={
                    'title': movie_data['title'],
                    'description': movie_data['description'],
                    'release_date': movie_data['release_date'],
                    'genre': movie_data['genre'],
                    'poster': movie_data['poster']
                }
            )
            if created:
                return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
            return Response({"message": "Movie already exists."}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to fetch movie data."}, status=status.HTTP_400_BAD_REQUEST)


class MovieList(APIView):
    """ All Movies List store on our database from TMDB """
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def get(self, request,format=None):
        page = CustomPagination()
        page_number = request.query_params.get('page', 1)
        user=User.objects.get(pk=request.user.id)
        movies=Movie.objects.filter(user= user)
        movies = page.paginate_queryset(movies, request)
        serialized_movies = MovieSerializer(movies, many=True).data
        info={
            'movies': serialized_movies,
            'total_pages': page.page.paginator.num_pages,
            'current_page':page.page.number,
        }
        
        return Response(info,status=status.HTTP_200_OK)



class FetchAndStoreMovies(APIView):
    """ Fetching All Movie From TMDB By Movie Type and Store into Our database """
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self, request,movie_type):
        
        if movie_type=='now_playing':
            m_type='now_playing'
        elif movie_type=='top_rated':
            m_type='top_rated'
        elif movie_type=='upcoming':
            m_type='upcoming'
        else:
            m_type='popular'

        movies_data = fetch_now_playing_movies(m_type)
        if movies_data:
            user_info=User.objects.get(pk=request.user.id)
            movies = []
            for movie_data in movies_data:
                movie, created = Movie.objects.get_or_create(
                    user=user_info,
                    movie_id=int(movie_data['id']),
                    defaults={
                        'title': movie_data['title'],
                        'description': movie_data['overview'],
                        'release_date': movie_data['release_date'],
                        'movie_type': m_type,
                        'genre': ', '.join([str(genre) for genre in movie_data.get('genre_ids', [])]),  # Adjust genre handling as needed
                        'poster':f"https://image.tmdb.org/t/p/w500/{movie_data.get('poster_path', '')}" 
                    }
                )
                movies.append(movie)

            serialized_movies = MovieSerializer(movies, many=True).data
            return Response({'movies': serialized_movies}, status=status.HTTP_201_CREATED)
        return Response({"error": "Failed to fetch now playing movies."}, status=status.HTTP_400_BAD_REQUEST)


class SearchMovie(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        keyword=request.data.get('keyword')
        page = CustomPagination()
        page_number = request.query_params.get('page', 1)
        user=User.objects.get(pk=request.user.id)
        movies=Movie.objects.filter(user= user)
        movies=movies.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(movie_type__icontains=keyword))
        movies = page.paginate_queryset(movies, request)
        serialized_movies = MovieSerializer(movies, many=True).data
        info={
            'movies': serialized_movies,
            'total_pages': page.page.paginator.num_pages,
            'current_page':page.page.number,
        }
        
        return Response(info,status=status.HTTP_200_OK)
    
class RecommendMovies(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        try:
            user_id = request.user.id
            user_reviews = get_user_reviews(user_id)
            movies = get_all_movies()
            num_users = len(set(review.user_id for review in user_reviews))
            ratings_matrix = prepare_ratings_matrix(user_reviews, movies)
            similarity_matrix = calculate_similarity(ratings_matrix)
            user_index = num_users - 1 
            similarity_scores = similarity_matrix[user_index]
        
            # Get indices of movies sorted by similarity (excluding already rated movies)
            movie_indices = np.argsort(similarity_scores)[::-1]
            print(movie_indices)
            # Filter out movies already rated by the user
            recommended_movies = [movies[int(idx)] for idx in movie_indices if ratings_matrix[user_index, idx]]
            serialized_movies = MovieSerializer(recommended_movies, many=True).data
            return Response({"movies":serialized_movies},status=status.HTTP_200_OK) 
        except:
            return Response({"movies":[]},status=status.HTTP_200_OK) 


# ========== MOVIE REVIEW API =============

class MovieReview(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        """ Create Movie review By Movie ID """
        serializer = MovieReviewSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user=User.objects.get(pk=request.user.id)
                m_id=serializer.data.get('movie')
                movie=Movie.objects.get(pk=m_id)
                rating=int(serializer.data.get('rating'))
                comment=serializer.data.get('comment')
                review = Review.objects.create(
                    user = user,
                    movie =  movie,
                    rating = rating,
                    comment = comment,
                )
                return Response({'msg':'Review created Successfully!'},status=status.HTTP_201_CREATED)
            except:
                return Response({"errors:Can't be created review please try again!"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,format=None):
        """ Get All Review with pagination """
        page = CustomPagination()
        page_number = request.query_params.get('page', 1)
        user=User.objects.get(pk=request.user.id)
        review=Review.objects.filter(user=user)
        review = page.paginate_queryset(review, request)
        serialized_review = MovieReviewSerializer(review, many=True).data
        info={
            'review': serialized_review,
            'total_pages': page.page.paginator.num_pages,
            'current_page':page.page.number,
        }
        
        return Response(info,status=status.HTTP_200_OK)
    
    def delete(self,request,format=None):
        """ Delete review By ID """
        id=request.data['id']
        try:
            if Review.objects.filter(pk=id).exists():
                Review.objects.filter(pk=id).delete()
            return Response({"msg":"Review has been deleted!"},status=status.HTTP_200_OK)
        except:
            return Response({"error":"Review can't be deleted!"},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,format=None):
        """ Update Review Information """
        serializer = MovieReviewUpdateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                rating=int(serializer.data.get('rating'))
                comment=serializer.data.get('comment')
                id=request.data.get('id')
                review = Review.objects.filter(pk=id).update(
                    rating = rating,
                    comment = comment,
                )
                return Response({'msg':'Review  Successfully updated!'},status=status.HTTP_202_ACCEPTED)
            except:
                return Response({"errors:Review Can't be Updated please try again later!"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class SearchReview(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        keyword=request.data.get('keyword')
        page = CustomPagination()
        page_number = request.query_params.get('page', 1)
        user=User.objects.get(pk=request.user.id)
        review=Review.objects.filter(user= user)
        review=review.filter(Q(rating__icontains=keyword) | Q(comment__icontains=keyword))
        review = page.paginate_queryset(review, request)
        serialized_review = MovieReviewSerializer(review, many=True).data
        info={
            'review': serialized_review,
            'total_pages': page.page.paginator.num_pages,
            'current_page':page.page.number,
        }
        
        return Response(info,status=status.HTTP_200_OK)
        