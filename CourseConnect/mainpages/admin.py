from django.contrib import admin
from . models import Course, Skill, Profile, Review
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Course)
admin.site.register(Skill)
admin.site.register(Review)
admin.site.register(Profile)

#Connect Profile and User info
class ProfileInline(admin.StackedInline):
    model = Profile

#Extend the User model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)