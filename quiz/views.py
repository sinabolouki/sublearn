from django.shortcuts import render
from .models import Quiz, QuizAttempt, QuestionAttempt
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.utils import timezone
from django.contrib import messages


# Create your views here.


def quiz_test(request, question_id):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        quiz = Quiz.load()
        try:
            quiz_attempt = QuizAttempt.objects.get(student=request.user)
        except QuizAttempt.DoesNotExist:
            return HttpResponseNotFound('no attempts')
        if quiz_attempt.date < timezone.now() + timezone.timedelta(minutes=quiz.time_minutes):
            quest_attempt = QuestionAttempt.objects.update_or_create(question_id=question_id, attempt=quiz_attempt,
                                                                     defaults={'response': request.field})
            quest_attempt.save()
        return
