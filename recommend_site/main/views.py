from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(response):
    return render(response, "main/base.html", {})

# redirects to the login page if not logged in
@login_required(login_url='/login/')
def home(response):
    return render(response, "main/home.html", {})