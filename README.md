# Movie Review and Recommendation API
This project is a Movie Review and Recommendation API built with Django REST framework. It fetches movie data from The Movie Database (TMDB) API and stores it in a SQLite database.

## Features

- Fetches movie data from TMDB API
- Provides endpoints for movie reviews and recommendations
- User authentication
- API documentation with Swagger and ReDoc

## Requirements

- Python 3.10
- Django
- Django REST framework
- SQLite
- `requests` library for fetching data from TMDB

## Setup

1. Clone the repository:

```
git clone https://github.com/rajvermadeveloper/MovieAPI.git
cd MovieAPI
```

2. Create a Python virtual environment in the MovieAPI folder.

```
python -m venv venv

```

3. Install the required packages:

```
pip install -r requirements.txt

```

4. Set up your TMDB API key:
Create a .env file in the project root and add your TMDB API key:

```
TMDB_API_KEY=your_tmdb_api_key
TMDB_ACCESS_TOKEN=your_tmdb_access_token
```
**LINK:** https://www.themoviedb.org/

4. Run migrations:

```
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:

```
python manage.py runserver

```


## API Documentation
The API documentation is available at the following URLs:
* Swagger UI
* ReDoc
* Swagger JSON

## LINK OF DOCS
* http://localhost:8000/swagger/
* http://localhost:8000/swagger.json/
* http://localhost:8000/redoc/

## Authentication
The API uses token-based authentication. To obtain a token, use the following endpoint:
* POST /api/v1/user/signup/ - Register a new user
* POST /api/v1/user/signin/ - Authenticate and obtain a user token

Login and Signup by following Fields:

```
    {
        "email":"rajverma12@gmail.com",
        "name":"Raj Verma",
        "password":"123456",
        "password2":"123456",
        "tc":true #Terms & Conditions
    }
```

After Signup and Login, you are access Token Like This :

```
    {
        "token": {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxOTgyNDgwNywiaWF0IjoxNzE5NzM4NDA3LCJqdGkiOiJhNTgxZWQxYTZlYTI0ZTFlYWUzYjViYWVhZmU5ZTJiZCIsInVzZXJfaWQiOjZ9.7ZIVTKsb9BUmRSyYqgPsH1-LjRMn-P6Qrid8NC4R8Kk",
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NzM5NjA3LCJpYXQiOjE3MTk3Mzg0MDcsImp0aSI6IjJhOTRkZWI4NzVjNzRiZjg4MjU5NWQxYTI1N2I1NTJjIiwidXNlcl9pZCI6Nn0.X2-qb7eyERTPPUaKLZx9ztgSIRa4lCwk_ivI-omRFWw"
        },
        "msg": "Login Successfully!"
    }

```


Include the Access token in the Authorization header for authenticated requests:

```
Authorization: Bearer your_token
```

# Endpoints

## User Authentication
* POST /api/v1/user/signup/ - Register a new user
* POST /api/v1/user/signin/ - Authenticate and obtain a user token
* GET /api/v1/user/profile/ - Retrieve user profile information
* POST /api/v1/user/logout/ - Logout and invalidate current user session

## Movie Endpoints
* POST /api/v1/movies/popular - Fetch popular movies
* POST /api/v1/movies/top_rated - Fetch top-rated movies
* POST /api/v1/movies/upcoming - Fetch upcoming movies
* POST /api/v1/movies/now_playing - Fetch movies currently playing in theaters
* GET /api/v1/movies/?page=1 - List movies with pagination support
* POST /api/v1/search-movie/?page=1 - Search for movies with pagination support

## Recommend Movies
* GET /api/v1/recommend-movies/ - Get recommended movies based on user preferences

## Review Endpoints
* POST /api/v1/review/ - Create a new movie review
* GET /api/v1/review/?page=1 - List movie reviews with pagination support
* PUT /api/v1/review/ - Update an existing movie review
* DELETE /api/v1/review/ - Delete an existing movie review
* SEARCH /api/v1/search-review/?page=1 - Search movie reviews with pagination support


## Postman API documentation

**Link**: (https://documenter.getpostman.com/view/23890483/2sA3duFt5o)

