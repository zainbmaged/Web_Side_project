from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
##from django.http import HttpResponse
##from django.shortcuts import render

##here we add application urls to be connected to the ec folder urls(main urls)
urlpatterns = [
    path('', views.home),
    path('home', views.home, name = 'home'),
    path('register', views.register, name = 'register'),
    path('UserProfile', views.userprofile, name = 'userprofile'),
    path('base', views.base),
    path('courses', views.courses, name = 'courses'),
    path('login', views.login, name="login"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'app/password_reset.html'),
         name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'app/password_reset_sent.html'),
         name = "password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_form.html'),
         name = "password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name ='app/Password_reset_complete.html'),
         name = "password_reset_complete"),
]
