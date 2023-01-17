from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})

def login(response):
    if response.user.is_authenticated:
        return redirect("/home")
    else:
        if response.method == 'POST':
            form = AuthenticationForm(response.POST)
            if form.is_valid():
                form.save()
                return redirect('/home')
        else:
            form = AuthenticationForm()

    return render(response, "registration/login.html", {"form": form})
