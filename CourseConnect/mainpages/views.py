from urllib import request
from django.shortcuts import render
from django.views import View
from . models import Course

def homepage(request):
    return render(request, 'pages/HomePage.html')

def loginpage(request):
    return render(request, 'pages/LoginPage.html')

def registerpage(request):
    return render(request, 'pages/RegisterPage.html')

def userprofile(request):
    return render(request, 'pages/UserProfile.html')

def allcourses(request):
    courses_list = Course.objects.all()
    context = {'courses_list': courses_list}
    return render(request, 'pages/CoursesList.html', context)

def Businesscategory(request):
    b1 = Course.objects.filter(Category='Business & Management').values()
    b2 = Course.objects.filter(Category='Business').values()
    b3 = Course.objects.filter(Category='School of business').values()
    b4 = b1 | b2 | b3
    context = {'Business_Category': b4}
    return render(request, 'pages/Business-and-Management.html', context)

def DataSciencecategory(request):
    b1 = Course.objects.filter(Category='Data Science').values()
    b2 = Course.objects.filter(Category='Data Analysis & Statistics').values()
    b3 = Course.objects.filter(Category='School of data science').values()
    b4 = b1 | b2 | b3
    context = {'DataScience_Category': b4}
    return render(request, 'pages/Data-Science.html', context)