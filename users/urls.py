
from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

app_name = "users"

urlpatterns = [
    path('', views.user_home, name='home'),
    path(r'register/', views.user_register, name="register"),
    path(r'profile/', views.user_profile, name="profile"),
    path(r'login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path(r'confirm/', auth_views.LogoutView.as_view(template_name='users/confirm.html'), name="confirm"),
    path(r'quize/', auth_views.LogoutView.as_view(template_name='users/quiz.html'), name="quiz"),
    path(r'forgotPassword/', auth_views.LogoutView.as_view(template_name='users/forgotPassword.html'), name="forgotPassword"),
    path(r'index/', views.user_index, name='index'),
    path(r'', views.user_index, name='index'),
    path(r'send_signup_code/', views.send_code, name='send_signup_code')
]
