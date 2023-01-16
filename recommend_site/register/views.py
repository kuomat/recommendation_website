from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
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

def change_password(response, user_id):
    if response.method == 'POST':
        user = User.objects.get(pk=user_id)
        form = SetPasswordForm(user, response.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(response, user)
            messages.success(response, 'Your password was successfully updated!')
            return redirect('/login')

    else:
        form = SetPasswordForm(response.user)
    return render(response, "register/change_password.html", {"form": form})