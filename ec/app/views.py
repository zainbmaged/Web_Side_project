from django.shortcuts import render

# Create your views here. (front end pages)

def home(request):
    return render(request,"app/index.html")