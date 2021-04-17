from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from .models import User
from .forms import LoginForm


def home(request):
    return render(request, 'users/home.html')


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        context = {}

        if not (name and email and password and re_password):
            context['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            context['error'] = '비밀번호가 다릅니다.'
        else:
            user = User(
                name=name,
                email=email,
                password=make_password(password)
            )

            user.save()

        return render(request, 'users/register.html', context)
