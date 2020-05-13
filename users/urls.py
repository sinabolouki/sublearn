from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

app_name="users"

urlpatterns = [
    path('', views.user_home, name='home'),
    path(r'register/', views.user_register, name="register"),
    path(r'profile/', views.user_profile, name="profile"),
    path(r'login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path(r'index/', views.user_index, name='index'),
]
