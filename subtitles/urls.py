from django.urls import path

from subtitles import views

app_name="subtitles"

urlpatterns = [
    path('', views.sub_processor, name='sub_processor'),
    path('download_sub', views.download_sub, name='download_sub'),
    path('download_words_list', views.download_words_list, name='download_words_list'),
]
