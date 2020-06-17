from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from flashcards.models import Flashcard
import random
from .models import Exam, ExamQuestion
# Create your views here.


@login_required()
def create_exam(request):
    flashcards = Flashcard.objects.filter(movie__user_id=request.user.id)
    flash_ids = list(flashcards.values_list('id', flat=True))
    n = 10
    rand_ids = random.sample(flash_ids, min(len(flash_ids), n))
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
    data = {'questions': exams}
    return JsonResponse(data)


@login_required()
def calc_result(request):
    exam_id = request.POST.get('id')
    result = request.POST.get('result')
    try:
        exam = Exam.objects.get(id= exam_id)
        if result is not None and result != '' and result != 'null':
            exam.result = float(result)
            exam.save()
            return JsonResponse({'response': 'success'})
        return JsonResponse({'response': 'error', 'error_message': 'no result sent'})
    except Exam.DoesNotExist:
        return JsonResponse({'response': 'error', 'error_message': 'no exam with this id'})
