from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here. (front end pages)

def base(request):
    return render(request,"app/base.html")

def courses(request):
    return render(request,"app/courses.html")

def home(request):
    return render(request,"app/index.html")

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
               messages.info(request, 'Email Already Exists') 
               return redirect('register')
            else:
                user = User.objects.create_user(username = email, email = email, password = password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Different passwords')    
            return redirect('register')
    else:    
        return render(request, 'app/register.html')

def userprofile(request):
    return render(request, "app/UserProfile.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username = username , password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('userprofile')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:    
        return render(request, "app/login.html")
    
#def resetPassword(request):
 #    return render(request,"app/login/resetPassword.html")
