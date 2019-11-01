from django.db import models
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=20)

class Movie(models.Model):
    title = models.CharField(max_length=20)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=50)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class Review(models.Model):
    content = models.CharField(max_length=50)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
