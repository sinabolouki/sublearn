from django.db import models
from django.contrib.auth.models import User
from flashcards.models import Flashcard


# Create your models here.


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    number = models.IntegerField()
    word = models.CharField(max_length=100)
    right_answer = models.CharField(max_length=100)
    answer_2 = models.CharField(max_length=100)
    answer_3 = models.CharField(max_length=100)
    answer_4 = models.CharField(max_length=100)

