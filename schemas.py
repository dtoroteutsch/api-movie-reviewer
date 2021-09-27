from pydantic import BaseModel, validator
from pydantic.utils import GetterDict

from typing import Any
from peewee import ModelSelect

from datetime import date

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any=None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

# -------------- User -------------------

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud debe encontrarse entre 3 y 50 caracteres')
        return username

class UserResponseModel(ResponseModel):
    id: int
    username: str

# -------------- Movie -------------------

class MovieRequestModel(BaseModel):
    title: str
    release_date: date
    language: str

    @validator('title')
    def title_validator(cls, title):
        if len(title) < 3 or len(title) > 50:
            raise ValueError('La longitud del titulo debe encontrarse entre 3 y 50 caracteres')
        return title

    @validator('language')
    def language_validator(cls, language):
        if len(language) > 20:
            raise ValueError('La longitud del lenguage no puede ser superior a 20 caracteres')
        return language

class MovieResponseModel(ResponseModel):
    title: str
    release_date: date
    language: str

# ------------- Review ------------------

class ReviewValidatorModel():
    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('Los rangos de valoración deben encontrarse entre el rango 1 y 5')
        return score

class ReviewRequestModel(BaseModel, ReviewValidatorModel):
    user_id: int
    movie_id: int
    review: str
    score: int

class ReviewResponseModel(ResponseModel):
    movie: MovieResponseModel
    review: str
    score: int

class ReviewRequestPutModel(BaseModel, ReviewValidatorModel):
    review: str
    score: int

