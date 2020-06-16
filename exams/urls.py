
from . import views
from django.urls import path

app_name = 'exams'

urlpatterns = [
    path('create/', views.create_exam, name='create_exam'),
    path('result/', views.calc_result, name='calc_result'),
]
