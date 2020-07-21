from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
import random
import re
from django.utils import timezone

from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm, SignupForm
from .tokens import account_activation_token
from .models import User, EmailCode, Profile


def user_home(request):
    context = {
        "title": "User Home",
    }
    print(request.META)
    return render(request, 'users/home.html', context=context)


@login_required()
def get_quiz(request):
    premium = request.user.profile.premium_date
    if premium < timezone.now():
        return render(request, 'flashcards/quiz.html', {'is_premium': False})
    return render(request, 'users/quiz.html', {'is_premium': True})


def user_register(request):
    if request.method == 'POST':
        print('Hello', request.POST.get('email'))
        code = random.randint(100000, 999999)
        email = request.POST.get('email')
        now = timezone.now()
        if User.objects.filter(email=email).exists():
            messages.error(request, f'a user already exists with this email')
            return render(request, 'users/signupEmail.html')
        try:
            code_obj = EmailCode.objects.get(email=email)
            if code_obj.date_changed + timezone.timedelta(minutes=2) > now:
                messages.error(request, f"code not sent to {email}: last code is not expired yet")
                return render(request, 'users/signupEmail.html')
            else:
                code_obj.code = code
                code_obj.save()
        except EmailCode.DoesNotExist:
            code_obj = EmailCode.objects.create(email=email, code=code)
            code_obj.save()
        recipient_list = [email, ]
        subject = 'Sublearn Forget Password Code'
        message = 'Hello \n Your Signup code is ' + str(code) + '. \n \n Thank you for your registration.' \
                                                                '\n Sublearn Team'
        email_from = settings.EMAIL_HOST_USER
        res = send_mail(subject, message, email_from, recipient_list)
        if res == 1:
            messages.success(request, f"Email with code sent to {email}! ")
        context = {
            "title": 'Signup code',
            "email": email
        }
        return render(request, 'users/confirm.html', context=context)
        # if form.is_valid():
        #     form.save()
        #     username = form.cleaned_data.get('username')
        #     messages.success(request, f"Account created for {username}! You can login now")
        #     return redirect("users:login")
        # else:
        #     print('hello')
    else:
        form = UserRegisterForm()

    # context = {
    #         "title": "User Register",
    #         "form": form
    #         }
    return render(request, 'users/signupEmail.html')


@login_required
def user_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("users:profile")

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile1.html', context={'forms': [u_form, p_form], 'title': 'Profile',
                                                           'quiz_res': request.user.profile.quiz_score})


def forgot_password(request):
    if request.method == 'POST':
        code = random.randint(100000, 999999)
        email = request.POST.get('email')
        now = timezone.now()
        if User.objects.filter(email=email).exists():
            # TODO: should return error
            print('filan')
        try:
            code_obj = EmailCode.objects.get(email=email)
            if code_obj.date_changed + timezone.timedelta(minutes=2) > now:
                # TODO: error
                print('felan')
            else:
                code_obj.code = code
                code_obj.save()
        except EmailCode.DoesNotExist:
            code_obj = EmailCode.objects.create(email=email, code=code)
            code_obj.save()
        subject = 'Sublearn Forget Password Code'
        message = 'Hello \n Your Signup code is ' + str(code) + '. \n \n Thank you for your registration.' \
                                                                '\n Sublearn Team'
        email_reg = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email_from = settings.EMAIL_HOST_USER
        if re.search(email_reg, email):
            recipient_list = [email, ]
        else:
            recipient_list = []
        send_mail(subject, message, email_from, recipient_list)
        return
    return render(request, 'users/forgotPassword.html', context={'title': 'Forget Password'})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'users/sentCode.html')
    else:
        form = SignupForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')


def user_index(request):
    return render(request, 'index.html')


def quiz_result(request):
    if request.method == 'POST':
        result = request.POST.get('result')
        try:
            user = request.user
            user.profile.quiz_score = float(result)
            user.profile.save()
            user.save()
        except User.DoesNotExist:
            data = {'response': 'error',
                    'error_message': 'no user found with this id'}
            return JsonResponse(data)
        data = {'response': 'success'}
        return JsonResponse(data)


def get_exam(request):
    premium = request.user.profile.premium_date
    if premium < timezone.now():
        return render(request, 'flashcards/exam.html', {'is_premium': False})
    return render(request, 'users/exam.html', {'is_premium': True})
