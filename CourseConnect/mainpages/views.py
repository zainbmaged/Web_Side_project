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
import sys
sys.path.append("..")
from model import ContentBasedModel

## for recommendation model
from django.db.models import F
import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from CourseConnect.settings import BASE_DIR
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
    return render(request, 'pages/courses.html', {'courses': courses})

def courses(request):
    if request.method == 'POST':
        inputValue = request.POST['inputValue']
        searched = Course.objects.filter(Q(Title__icontains=inputValue) | Q(Price__icontains=inputValue) | Q(Platform__icontains=inputValue))
        return render(request, 'pages/courses.html', {'searched': searched, 'inputValue':inputValue})
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
               messages.info(request, 'Email Already Exists')
               return redirect('register')
            else:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, (f"Account created for {username} successfully.\nWelcome!"))
                return redirect('homepage')
        else:
            messages.success(request, ("An error occured. Please try again."))
            return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'pages/RegisterPage.html', {'form': form})


@login_required
def userprofile(request, foo):
    #Replace hyphens with spaces.
    #foo = foo.replace('-', ' ')
    if request.user.is_authenticated and request.user.username == foo:
        try:
            user = User.objects.get(username=foo)
            reviews = Review.objects.filter(user=request.user)
            userCourses = user.profile.takenCourses.all().filter()
            takenCourses = []
            for i in userCourses:
                takenCourses.append(i.Title)
            recommendation = ContentBasedModel.get_recommendations(takenCourses)
            context = {'user': user, 'reviews': reviews, 'recommendation': recommendation}
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
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
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
        if self.request.user == review.user:
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
        if self.request.user == review.user:
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
    if request.method == 'POST':
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

@login_required
def getRecommendation(request, foo):
    if request.user.is_authenticated and request.user.username == foo:
        try:
            user = User.objects.get(username=foo)
            userCourses = user.profile.takenCourses.all().filter()
            takenCourses = []
            for i in userCourses:
                takenCourses.append(i.Title)
            recommendation = ContentBasedModel.get_recommendations(takenCourses)
            courses = Course.objects.filter(Q(Title__in=recommendation)).distinct()
            context = {'courses': courses, 'user': user, 'takenCourses': takenCourses, 'recommendation': recommendation}
            return render(request, 'pages/Recommendation.html', context)
        except:
            messages.success(request, ("Sorry, this username does not exist."))
            return redirect('homepage')
    else:
        messages.success(request, ("Sorry, you cannot access this page."))
        return redirect('homepage')

## collaborative model ----------------------------------------------------------------------------------------------

def define_label_encoders(all_courses):
    label_encoders = []
    fields = ['Level', 'Language', 'Platform', 'Certificate', 'Duration', 'Category', 'Learning_Type', 'Instructors']
    for field in fields:
        # Collect all unique values for the field
        unique_values = set(getattr(course, field) for course in all_courses)
        # Define and fit label encoder for the field
        label_encoder = LabelEncoder()
        label_encoder.fit(list(unique_values))
        label_encoders.append(label_encoder)
    return label_encoders

def train_random_forest_regressor(reviewed_courses, label_encoders):
    # Collect features and target variable
    features = []
    ratings = []
    fields = ['Level', 'Language', 'Platform', 'Certificate', 'Duration', 'Category', 'Learning_Type', 'Instructors']
    for course in reviewed_courses:
        # Extract features
        feature_vector = [getattr(course, field) for field in fields]
        features.append(feature_vector)
        # Extract target variable
        ratings.append(course.rating)

    # Convert lists to numpy arrays
    X = np.array(features)
    y = np.array(ratings)

    # Apply label encoding to categorical features
    for i, label_encoder in enumerate(label_encoders):
        X[:, i] = label_encoder.transform(X[:, i])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)
    params = {
        "n_estimators": 200,
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1
    }

    # Train the Random Forest regressor
    regressor = RandomForestRegressor(**params, random_state=13)
    regressor.fit(X_train, y_train)

    # Evaluate the regressor
    y_pred = regressor.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return regressor

def predict_top_rated_courses(unrated_courses, regressor, label_encoders, top_n=20):
    # Collect features for unrated courses
    features = []
    fields = ['Level', 'Language', 'Platform', 'Certificate', 'Duration', 'Category', 'Learning_Type', 'Instructors']
    for course in unrated_courses:
        # Extract features
        feature_vector = [getattr(course, field) for field in fields]
        features.append(feature_vector)

    # Convert features to numpy array
    X = np.array(features)

    # Apply label encoding to categorical features
    for i, label_encoder in enumerate(label_encoders):
        # Transform, ignoring unseen labels
        X[:, i] = label_encoder.transform(X[:, i])
        # Handle unseen labels
        unknown_mask = X[:, i] == -1
        if np.any(unknown_mask):
            # Replace unseen labels with a default value or handle them accordingly
            X[unknown_mask, i] = label_encoder.transform(['<unknown>'])[0]

    # Make predictions
    ratings_predicted = regressor.predict(X)

    # Combine predicted ratings with unrated courses
    courses_with_ratings = list(zip(unrated_courses, ratings_predicted))

    # Sort courses based on predicted ratings (descending order)
    courses_with_ratings.sort(key=lambda x: x[1], reverse=True)

    # Get top rated courses with titles
    top_rated_courses_decoded = []
    for course, rating in courses_with_ratings[:top_n]:
        decoded_course = {
            'Title': course.Title,
            'Level': label_encoders[0].inverse_transform([X[0, 0].astype(int)])[0],  
            'Language': label_encoders[1].inverse_transform([X[0, 1].astype(int)])[0],  
            'Rating': course.Rating,
            'Platform': label_encoders[2].inverse_transform([X[0, 2].astype(int)])[0],  
            'Certificate': label_encoders[3].inverse_transform([X[0, 3].astype(int)])[0],  
            'Duration': label_encoders[4].inverse_transform([X[0, 4].astype(int)])[0],  
            'Category': label_encoders[5].inverse_transform([X[0, 5].astype(int)])[0],  
            'Learning_Type': label_encoders[6].inverse_transform([X[0, 6].astype(int)])[0],  
            'Instructors': label_encoders[7].inverse_transform([X[0, 7].astype(int)])[0],  
            'Predicted Rating': rating
        }
        top_rated_courses_decoded.append(decoded_course)

    return top_rated_courses_decoded

class RecommendationPage(LoginRequiredMixin,ListView):
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
        label_encoders=define_label_encoders(all_courses)
      
        # Query to retrieve course details for the reviewed courses
        reviewed_courses = Course.objects.filter(review__user=user).annotate(rating= F('review__rating'))
        # Call the train_random_forest_regressor function
        regressor = train_random_forest_regressor(reviewed_courses,label_encoders)
        unrated_courses = Course.objects.exclude(review__user=user)

        top_rated_courses_decoded=predict_top_rated_courses(unrated_courses, regressor, label_encoders)


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