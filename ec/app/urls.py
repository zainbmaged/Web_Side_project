from django.urls import path
from . import views
##from django.http import HttpResponse
##from django.shortcuts import render

##here we add application urls to be connected to the ec folder urls(main urls)
urlpatterns = [
    path('', views.home),
    path('register.html', views.register),
    path('UserProfile.html', views.userprofile),
]
