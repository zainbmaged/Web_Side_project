from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
from django.urls import reverse
import datetime
from PIL import Image

#Courses Skills (General categories). 
class Skill(models.Model):
    Type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Type
    

#All Courses.
class Course(models.Model):
    Title = models.CharField(max_length=500)
    Rating = models.CharField(max_length=100, default=None, null=True, blank=True)
    Level = models.CharField(max_length=50)
    Language = models.CharField(max_length=500)
    Price = models.CharField(max_length=500, default=None, null=True, blank=True)
    URL = models.CharField(max_length=500)
    Image = models.ImageField(upload_to='Images/course_pics', default='Images/pictureplaceholder.jpg', null=True, blank=True)
    Description = models.CharField(max_length=1500)
    Platform = models.CharField(max_length=50)
    Certificate = models.CharField(max_length=100, default=None, null=True, blank=True)
    Duration = models.CharField(max_length=500, default=None, null=True, blank=True)
    Learning_Type = models.CharField(max_length=500, default=None, null=True, blank=True)
    Enrolled = models.CharField(max_length=500, default=None, null=True, blank=True)
    Reviews = models.CharField(max_length=500, default=None, null=True, blank=True)
    Last_Updated = models.CharField(max_length=500, default=None, null=True, blank=True)
    Category = models.CharField(max_length=100)
    Instructors = models.CharField(max_length=500)
    Skill = models.ForeignKey(Skill, on_delete=models.CASCADE, default=1, null=True)
    #Organization = models.CharField(max_length=500)

    def __str__(self):
        return self.Title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    fullreview = models.CharField(max_length=600)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Course: {self.course.Title} --> Rating: {self.rating}"
    
    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})
    


#Users Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    image = models.ImageField(upload_to='Images/profile_pics', default='Images/defaultprofile.jpg', null=True, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    LANGUAGE_CHOICES = (('E', 'English'), ('A', 'Arabic'), ('K', 'Korean'), ('G', 'German'))
    language = models.CharField(max_length=1, choices=LANGUAGE_CHOICES, null=True, blank=True)
    #skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
    #liked = models.ForeignKey(Like, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 350:
            output_size = (350, 350)
            img.thumbnail(output_size)
            img.save(self.image.path)


#Users
'''class myUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField()
    LANGUAGE_CHOICES = (('E', 'English'), ('A', 'Arabic'), ('K', 'Korean'), ('G', 'German'))
    language = models.CharField(max_length=1, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
'''
'''
class Instructor(models.Model):
    Name = models.CharField(max_length=500)
    Organization = models.CharField(max_length=500)
    Field = models.CharField(max_length=500)
    Rating = models.DecimalField(max_digits=10, decimal_places=2)
    Total_Courses = models.IntegerField()
'''