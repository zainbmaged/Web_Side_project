from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here. (front end pages)

def home(request):
    return render(request,"app/index.html")

def register(request):
    return render(request, 'app/register.html')

def userprofile(request):
    return render(request, "app/UserProfile.html")

def login(request):
    return render(request, "app/login.html")

