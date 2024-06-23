from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from . views import ReviewListView, ReviewDetailView, UserReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, CourseListView, rate_course, UserCourseListView, RecommendationPage

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    #path('register', views.register, name='register'),
    path('checkbox', views.checkbox, name='checkbox'),
    #path('skills', views.profile_skills, name='skills'),
    #======================================================================================================================================================================#
    path('userprofile/<str:foo>', views.userprofile, name='userprofile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('update_info', views.update_info, name='update_info'),
    path('update_password', views.update_password, name='update_password'),
    #======================================================================================================================================================================#
    #path('allcourses', views.allcourses, name='allcourses'),
    path('course/<int:pk>', views.course, name='course'),
    path('category/<str:foo>', views.category, name='category'),
    path('search', views.search, name='search'),
    path('courses/<str:username>', UserCourseListView.as_view(), name='user-courses'),
    path('filters', views.filters_view, name='filters'),
    #======================================================================================================================================================================#
    path('user/<str:username>', UserReviewListView.as_view(), name='user-reviews'),
    path('allreviews', ReviewListView.as_view(), name='allreviews'),
    #path('allreviews/<str:foo>', UserReviewListView.as_view(), name='userreviews'),
    path('addreview/<int:pk>', views.addreview, name='addreview'),
    path('review/<int:pk>', ReviewDetailView.as_view(), name='review-detail'),
    path('review/new', ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:pk>/update', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete', ReviewDeleteView.as_view(), name='review-delete'),
    path('rate/', rate_course, name='rate-view'),
    #======================================================================================================================================================================#
    path('allcourses', CourseListView.as_view(), name="allcourses"),
    path('courses', views.courses, name = 'courses'),
    #======================================================================================================================================================================#
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'pages/password_reset.html'), name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'pages/password_reset_sent.html'), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'pages/password_reset_form.html'), name = "password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name ='pages/password_reset_complete.html'), name = "password_reset_complete"),
    #======================================================================================================================================================================#
    ##---Recommendation---##
    path('recommendation/<str:foo>', views.getRecommendation, name='recommendations'),
    path('recommendations/<str:username>', RecommendationPage.as_view(), name='recommendation_page'),
]