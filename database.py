from peewee import *
from datetime import datetime, date

import hashlib

database = MySQLDatabase('fastapi_project',
                        user='root',
                        password='1Nw4rd180',
                        host='127.0.0.1',
                        port=33060)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        table_name = 'users'

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

class Movie(BaseModel):
    title = CharField(max_length=70)
    release_date = DateField()
    language = CharField(max_length=20)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        table_name = 'movies'

class UserReview(BaseModel):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews')
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'

    class Meta:
        table_name = 'user_reviews'

