from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=500, null=True)
    genres = models.ManyToManyField(Genre, related_name='movie_genre')
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=200)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=500, null=True)
    release_date = models.DateField()
    title = models.CharField(max_length=200)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    

class Review(models.Model):
    title = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews', blank=True)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

