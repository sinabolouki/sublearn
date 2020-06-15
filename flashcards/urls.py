from django.urls import path

from flashcards import views

app_name = "flashcards"

urlpatterns = [
    path('', views.load_decks, name='load_decks'),
    path('<int:set_id>/', views.show_flashcards, name='show_flashcards'),
    path('result/', views.flashcard_result, name='flashcard_result')
]
