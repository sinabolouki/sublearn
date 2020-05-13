from django.db import models
from django.contrib.auth.models import User


class MovieSet(models.Model):
    movie_name = models.CharField(max_length=100)
    date_added = models.DateTimeField('date added', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_name


class Flashcard(models.Model):
    english_word = models.CharField(max_length=30)
    translation = models.CharField(max_length=30)
    movie = models.ForeignKey(MovieSet, on_delete=models.CASCADE)
    last_viewed_time = models.DateTimeField('date reviewed', auto_now=True)
    last_time_remembered = models.BooleanField(default=False)
    times_remembered = models.IntegerField(default=0)
    times_failed = models.IntegerField(default=0)

    def __str__(self):
        return self.english_word
