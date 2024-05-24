from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from . models import Course, Skill, Profile, Review
from django.contrib.auth.models import User, auth
from django import forms
from . forms import UserRegisterForm, ChangePasswordForm, UserInfoForm, UserUpdateForm, ProfileUpdateForm, UserReviewForm
from django.http import JsonResponse, HttpResponse
from itertools import chain
import json
import datetime
##---for recommendation models---##
import sys
sys.path.append("..")
from model import ContentBasedModel, RandomForest
from django.db.models import F


def homepage(request):
    #setvalue()
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'pages/HomePage.html', context)

def course(request, pk):
    course = Course.objects.get(id=pk)
    context = {'course': course}
    return render(request, 'pages/Course.html', context)

def allcourses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'pages/courses.html', context)

def courses(request):
    if request.method == 'POST':
        inputValue = request.POST['inputValue']
        searched = Course.objects.filter(Q(Title__icontains=inputValue) | Q(Price__icontains=inputValue) | Q(Platform__icontains=inputValue))
        context = {'searched': searched, 'inputValue':inputValue}
        return render(request, 'pages/courses.html', context)
    else:
        return render(request, 'pages/courses.html')

def category(request, foo):
    #Replace hyphens with spaces.
    foo = foo.replace('-', ' ')
    try:
        category = foo.lower()
        courses1 = Course.objects.filter(Category=foo)
        courses2 = Course.objects.filter(Category=category)
        course = list(chain(courses1, courses2))
        length = len(course)
        if (10 <= length < 50):
            pages = Paginator(course, 10)
        elif (25 < length <= 50):
            pages = Paginator(course, 25)
        else:
            pages = Paginator(course, 50)
        page_number = request.GET.get('page') #Get the requested page number from the URL
        page = pages.get_page(page_number)
        courses = page.object_list
        context = {'courses': courses, 'category': foo, 'page': page, 'length': length}
        return render(request, 'pages/Category.html', context)
    except:
        messages.success(request, ("Sorry, this category does not exist."))
        return redirect('homepage')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in successfully."))
            return redirect('homepage')
        else:
            messages.success(request, ("Invalid Credentials. Please Try again."))
            return redirect('login')
    else:
        return render(request, 'pages/LoginPage.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out successfully.\n\nThank you!"))
    return redirect('homepage')

def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data.get('email')).exists():
               messages.info(request, 'Email Already Exists. Please Try Again')
               return redirect('register')
            else:
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                messages.success(request, (f"Account created for {username} successfully.\nWelcome!"))
                return redirect('homepage')
        else:
            messages.success(request, ("An error occured. Please try again."))
            return redirect('register')
    else:
        form = UserRegisterForm()
    
    return render(request, 'pages/RegisterPage.html', {'form': form})

'''
@login_required
def profile_skills(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            current = Profile_Skill.objects.create(user_id=request.user.id)
            form = ProfileSkillForm(request.POST, current)
            if form.is_valid():
                form.save(commit=False)
                form.save_m2m()
                return redirect('userprofile', foo=request.user.username)
            else:
                messages.success(request, ("An error occured. Please try again."))
                return redirect('pages/SkillsForm.html')
        else:
            form = ProfileSkillForm()
            return render(request, 'pages/SkillsForm.html', {"form":form})
    else:
        messages.success(request, ("Please log in first."))
        return render(request, 'pages/LoginPage.html', {"form":form})

def checkbox(request):
    if request.method=="POST":
        s = request.POST.getlist("chk[]")
        for s1 in s:
            print(s1)
        return render(request,"pages/SkillsCheckbox.html", {'key':s})
    return render(request,"pages/SkillsCheckbox.html")
'''

@login_required
def userprofile(request, foo):
    #Replace hyphens with spaces.
    #foo = foo.replace('-', ' ')
    if request.user.is_authenticated and request.user.username == foo:
        try:
            user = User.objects.get(username=foo)
            reviews = Review.objects.filter(user=request.user)
            #takenCourses = user.profile.takenCourses.all().filter()
            #titles = []
            #for i in range(len(reviews)):
            #    titles.append(reviews[i].course.Title)
            #recommendation = ContentBasedModel.get_recommendations(titles)
            #courses = Course.objects.filter(Q(Title__in=recommendation)).distinct()
            context = {'user': user,'reviews': reviews}
            return render(request, 'pages/UserProfile.html', context)
        except:
            messages.success(request, ("Sorry, this profile does not exist."))
            return redirect('homepage')
    else:
        messages.success(request, ("Sorry, you cannot access this page."))
        return redirect('homepage')
    
@login_required
def editprofile(request):
    if request.method == 'POST':
        old_email = request.user.email
        old_firstname = request.user.first_name
        old_lastname = request.user.last_name
        old_gender = request.user.profile.gender
        old_birthdate = request.user.profile.birthdate
        old_language = request.user.profile.language        
        
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            new_email = u_form.cleaned_data.get('email')
            new_firstname = u_form.cleaned_data.get('first_name')
            new_lastname = u_form.cleaned_data.get('last_name')
            new_gender = p_form.cleaned_data.get('gender')
            new_birthdate = p_form.cleaned_data.get('birthdate')
            new_language = p_form.cleaned_data.get('language')

            request.user.email = new_email if new_email != "" else old_email
            request.user.first_name = new_firstname if new_firstname != "" else old_firstname
            request.user.last_name = new_lastname if new_lastname != "" else old_lastname
            request.user.profile.gender = new_gender if new_gender != None else old_gender
            request.user.profile.birthdate = new_birthdate if new_birthdate != None else old_birthdate
            request.user.profile.language = new_language if new_language != None else old_language

            u_form.save()
            p_form.save()

            messages.success(request, (f"Account updated successfully."))
            return redirect('userprofile', foo=request.user.username)
        else:
            messages.success(request, ("An error occured. Please try again."))
            return redirect('editprofile')
    else:
        u_form = UserUpdateForm()
        p_form = ProfileUpdateForm()
    context = {"u_form":u_form, "p_form":p_form}
    return render(request, 'pages/EditProfile.html', context)
        
@login_required    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Password updated successfully!"))
                login(request, current_user)
                return redirect('editprofile')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'pages/UpdatePassword.html', {'form': form})
    else:
        messages.success(request, ("You must be logged in to access this page."))
        return redirect('homepage')

@login_required
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, ("Profile updated successfully!"))
            return redirect('userprofile')
        return render(request, 'pages/update_info.html', {'form': form})
    else:
        messages.success(request, ("You must be logged in to access this page."))
        return redirect('homepage')

'''
def allcourses(request):
    courses_list = Course.objects.all()
    categories = Skill.objects.all()
    context = {'courses_list': courses_list, 'categories': categories}
    return render(request, 'pages/CoursesList.html', context)
'''

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Course.objects.filter(Q(Title__icontains=searched) | Q(Price__icontains=searched))
        if not searched:
            messages.success(request, ("No data available.. please try again"))
            return render(request, 'pages/Search.html')
        else:
            return render(request, 'pages/Search.html', {'searched': searched})
    else:
        return render(request, 'pages/Search.html')
    
@login_required
def allreviews(request):
    context = {'reviews': Review.objects.all()}
    return render(request, 'pages/UserReviews.html', context)


class CourseListView(ListView):
    model = Course
    template_name = 'pages/CoursesList.html'
    context_object_name = 'courses'
    ordering = ['Title']
    paginate_by = 50


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'pages/AllReviews.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']
    paginate_by = 10

def rate_course(request):
    if request.method == "POST":
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        review = Review.objects.get(id=el_id)
        review.rating = val
        review.save()
        return JsonResponse({'success':'true', 'rating':val}, safe=False)
    return JsonResponse({'success':'true'})

class UserReviewListView(LoginRequiredMixin,ListView):
    model = Review
    template_name = 'pages/user_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 5

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user and review.course.Title in review.user.profile.takenCourses.all().filter():
            return True
        return False
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(user=user).order_by('-created_at')

class ReviewDetailView(DetailView):
    model = Review

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'fullreview', 'course']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['rating', 'fullreview', 'course']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        review = self.get_object()
        user = self.request.user
        course = review.course
        takenCourses = user.profile.takenCourses.all().filter()
        if self.request.user == review.user and course in takenCourses:
            return True
        return False
    
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user:
            return True
        return False

@login_required
def addreview(request, pk):
    course = Course.objects.get(id=pk)
    user = request.user
    takenCourses = user.profile.takenCourses.all().filter()
    if request.method == 'POST' and course in takenCourses:
        review = Review.objects.create(course_id=course.id, user_id=user.id)
        form = UserReviewForm(request.POST, instance=review)
        if form.is_valid():
            rating = form.cleaned_data.get('rating')
            fullreview = form.cleaned_data.get('fullreview')
            review.rating = rating
            review.fullreview = fullreview
            messages.success(request, (f"{review}"))
            form.save()
            messages.success(request, (f"Review added successfully."))
            return redirect('userprofile', foo=request.user.username)
        else:
            messages.success(request, ("An error occured.\nPlease try again."))
            return redirect('addreview', pk)
    else:
        form = UserReviewForm()
        messages.success(request, ("Invalid Review. User didn't take this course."))

    context = {'course': course, 'form':form}
    return render(request, 'pages/AddReview.html', context)

class UserCourseListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'pages/user_courses.html'
    context_object_name = 'profile'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Profile.objects.filter(user=user)


#---------Content-based Model---------#
@login_required
def getRecommendation(request, foo):
    if request.user.is_authenticated and request.user.username == foo:
        try:
            user = User.objects.get(username=foo)
            userCourses_rated = Review.objects.filter(user=request.user)
            titles = []
            for i in range(len(userCourses_rated)):
                titles.append(userCourses_rated[i].course.Title)
            recommendation = ContentBasedModel.get_recommendations(titles)
            courses = Course.objects.filter(Q(Title__in=recommendation)).distinct()
            context = {'courses': courses, 'user': user, 'takenCourses': titles, 'recommendation': recommendation}
            return render(request, 'pages/Recommendation.html', context)
        except:
            messages.success(request, ("Sorry, this username does not exist."))
            return redirect('homepage')
    else:
        messages.success(request, ("Sorry, you cannot access this page."))
        return redirect('homepage')

#---------Collaborative Model---------#
class RecommendationPage(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'pages/recommendation_page.html'
    context_object_name = 'reviews'
    paginate_by = 5

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user:
            return True
        return False
   
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        all_courses = Course.objects.all()
        label_encoders = RandomForest.define_label_encoders(all_courses)
      
        # Query to retrieve course details for the reviewed courses
        reviewed_courses = Course.objects.filter(review__user=user).annotate(rating = F('review__rating'))
        # Call the train_random_forest_regressor function
        regressor = RandomForest.train_random_forest_regressor(reviewed_courses,label_encoders)
        unrated_courses = Course.objects.exclude(review__user=user)
        
        top_rated_courses_decoded = RandomForest.predict_top_rated_courses(unrated_courses, regressor, label_encoders)

        return top_rated_courses_decoded

'''
def setvalue():
    skill = Skill.objects.filter(Type="Math").values()
    categ = skill[0]['Type']
    x = skill[0]['id']
    courses = Course.objects.filter(Category=categ).values()
    for course in courses:
       course.update(Skill__id=x)
    courses.update()
'''