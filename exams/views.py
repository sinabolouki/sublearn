from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from flashcards.models import Flashcard
import random
from .models import Exam, ExamQuestion
import numpy as np


# Create your views here.

def make_weights(n):
    x = np.arange(1, n + 1, dtype=np.float64)
    weights = 2 * n - x
    weights = weights / sum(weights)
    return weights


@login_required()
def create_exam(request):
    movie_id = request.POST.get('id')
    if movie_id is not None and movie_id != '' and movie_id != 'null':
        flashcards = Flashcard.objects.filter(movie_id=request.user.id).order_by('-times_failed',
                                                                                 'times_remembered')
    else:
        flashcards = Flashcard.objects.filter(movie__user_id=request.user.id).order_by('-times_failed',
                                                                                       'times_remembered')
    flash_ids = list(flashcards.values_list('id', flat=True))
    weights = make_weights(len(flash_ids))
    n = 10
    rand_ids_arr = np.random.choice(flash_ids, p=weights, size=(n,), replace=False)
    rand_ids = rand_ids_arr.tolist()
    random_cards = Flashcard.objects.filter(id__in=rand_ids)
    new_exam = Exam.objects.create(user_id=request.user.id)
    new_exam.save()
    exams = {}
    for card in random_cards:
        new_ques = ExamQuestion.objects.create(exam=new_exam)
        new_ques.word = card.english_word
        new_ques.right_answer = card.translation
        rem_cards = flashcards.exclude(id=card.id)
        rem_ids = list(rem_cards.values_list('id', flat=True))
        m = 3
        rand_ids = random.sample(rem_ids, m)
        rand_cards = Flashcard.objects.filter(id__in=rand_ids)
        new_ques.answer_2 = rand_cards[0].translation
        new_ques.answer_3 = rand_cards[1].translation
        new_ques.answer_4 = rand_cards[2].translation
        exams[card.english_word] = [card.translation, rand_cards[0].translation, rand_cards[1].translation,
                                    rand_cards[2].translation]
    print(exams)
    data = {'questions': exams, 'id': new_exam.id}
    return JsonResponse(data)


@login_required()
def calc_result(request):
    exam_id = request.POST.get('id')
    result = request.POST.get('result')
    try:
        exam = Exam.objects.get(id=exam_id)
        if result is not None and result != '' and result != 'null':
            exam.result = float(result)
            exam.save()
            return JsonResponse({'response': 'success'})
        return JsonResponse({'response': 'error', 'error_message': 'no result sent'})
    except Exam.DoesNotExist:
        return JsonResponse({'response': 'error', 'error_message': 'no exam with this id'})
