from django.urls import path

from subtitles import views
from django.views.generic import TemplateView

app_name="subtitles"

urlpatterns = [
    path('', views.sub_processor, name='sub_processor'),
    path('download_sub', views.download_sub, name='download_sub'),
    path('download_words_list', views.download_words_list, name='download_words_list'),
    path('download/', TemplateView.as_view(template_name='subtitles/download.html'), name='download_outside_sub')
]
