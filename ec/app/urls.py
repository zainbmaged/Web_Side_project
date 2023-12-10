 

from django.urls import path
from . import views


##here we add application urls to be connected to the ec folder urls(main urls)
urlpatterns = [
    path('', views.home),
]