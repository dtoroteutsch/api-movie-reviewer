from fastapi import FastAPI, HTTPException
from database import database as connection
from database import User, Movie, UserReview

from schemas import UserRequestModel, UserResponseModel
from schemas import ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel
from schemas import MovieRequestModel, MovieResponseModel

from typing import List

app = FastAPI(
        title = "Movie's reviews project",
        version = '1.0'
    )

@app.on_event('startup')
def startup():
    print('Starting the WebServer')
    if connection.is_closed():
        connection.connect()
        print('Starting DB connection...')

    connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    print('Stopping the WebServer')
    if not connection.is_closed():
        connection.close()
        print('Closing DB connection...')

@app.get('/hello')
async def hello():
    return 'Hello from FastAPI WebServer'

@app.get('/about')
async def about():
    return 'About'

# ------------------ Users ---------------------------

@app.post('/users', response_model=UserResponseModel)
async def create_user(user_request: UserRequestModel):
    # SELECT * FROM users WHERE users.id = ? LIMIT 1;
    if User.select().where(User.username == user.username).first():
        raise HTTPException(409, 'El nombre de usuario ingresado ya se encuentra registrado')

    hash_password = User.create_password(user_request.password)
    user = User.create(
        username = user_request.username,
        password = hash_password
    )
    #return UserResponseModel(id = user.id, username = user.username)
    return user

# ------------------ Movies -----------------------

@app.post('/movies', response_model=MovieResponseModel)
async def create_movie(movie_request: MovieRequestModel):
    movie = Movie.create(
        title = movie_request.title,
        release_date = movie_request.release_date,
        language = movie_request.language
    )
    return movie

@app.get('/movies', response_model=List[MovieResponseModel])
async def get_movies(page: int = 1, limit: int = 10):
    # SELECT * FROM movies;
    movies = Movie.select().paginate(page, limit)
    return [movie for movie in movies]

@app.get('/movies/{movie_id}', response_model=MovieResponseModel)
async def get_movie(movie_id: int):
    # SELECT * FROM movies WHERE movies.id = ? LIMIT 1;
    movie = Movie.select().where(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found')
    return movie

@app.put('/movies/{movie_id}', response_model=MovieResponseModel)
async def update_movie(movie_id: int, movie_request: MovieRequestModel):
    # SELECT * FROM movies WHERE movies.id = ? LIMIT 1;
    movie = Movie.select().where(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found')
    movie.title = movie_request.title
    movie.language = movie_request.language
    movie.release_date = movie_request.release_date
    movie.save()
    return movie

# ----------------- Reviews --------------------

@app.post('/reviews', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    # SELECT * FROM users WHERE users.id = ? LIMIT 1;
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail='User not found')
    # SELECT * FROM movies WHERE movies.id = ? LIMIT 1;
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail='Movie not found')
    user_review = UserReview.create(
        user_id = user_review.user_id,
        movie_id = user_review.movie_id,
        review = user_review.review,
        score = user_review.score
    )
    return user_review

@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    # SELECT * FROM user_reviews
    reviews = UserReview.select().paginate(page, limit)
    return [user_review for user_review in reviews]

@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    # SELECT * FROM user_reviews WHERE user_reviews.id = ? LIMIT 1
    user_review =  UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='Review not found')
    return user_review

@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    # SELECT * FROM user_reviews WHERE user_reviews.id = ? LIMIT 1
    user_review =  UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='Review not found')
    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()

    return user_review

@app.delete('/reviews/{review_id}')
async def delete_review(review_id: int):
    # SELECT * FROM user_reviews WHERE user_reviews.id = ? LIMIT 1
    user_review =  UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='Review not found')
    user_review.delete_instance()
    return user_review

