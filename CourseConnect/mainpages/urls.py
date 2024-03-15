from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.loginpage, name='login'),
    path('register', views.registerpage, name='register'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('allcourses', views.allcourses, name='allcourses'),
    path('Business-and-Management', views.Businesscategory, name='Business-and-Management'),
    path('Data-Science', views.DataSciencecategory, name='Data-Science'),
]