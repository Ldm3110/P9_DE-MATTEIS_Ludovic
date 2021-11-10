from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from . import forms
from .models import User


def login_view(request):
    auth = forms.UserForm()
    message = ""
    if request.method == 'POST':
        auth = forms.UserForm(request.POST)
        if auth.is_valid():
            user = authenticate(
                username=auth.cleaned_data['username'],
                password=auth.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                message = 'Les identifiants sont incorrects ! Réessayez ou inscrivez-vous svp'

    return render(request, 'connexion/login.html', context={'form': auth, 'mess': message})


def registration_view(request):
    message = ""
    register_form = forms.RegistrationForm()
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password2')
            user = User.objects.filter(username=username)
            if not user.exists():
                user = User.objects.create(
                    username=username,
                    password=make_password(password, 'salt', 'default')
                )
                login(request, user)
                return redirect('homepage')
            else:
                message = "L'utilisateur existe déjà !"

    return render(request, 'connexion/register.html', context={'form': register_form, 'mess': message})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
