from django.db import models

# Create your models here.
class Skill(models.Model):
    Type = models.CharField(max_length=800)

''' class Instructor(models.Model):
    Name = models.CharField(max_length=500)
    Organization = models.CharField(max_length=500)
    Field = models.CharField(max_length=500)
    Rating = models.DecimalField(max_digits=10, decimal_places=2)
    Total_Courses = models.IntegerField() '''

class Course(models.Model):
    Title = models.CharField(max_length=500)
    Rating = models.CharField(max_length=100)
    Level = models.CharField(max_length=50)
    Language = models.CharField(max_length=500)
    Price = models.CharField(max_length=500)
    URL = models.CharField(max_length=500)
    Image = models.ImageField(upload_to='Images/', default='Images/pictureplaceholder.jpg', null=True, blank=True)
    Description = models.CharField(max_length=500)
    Platform = models.CharField(max_length=50)
    Certificate = models.CharField(max_length=100)
    Duration = models.CharField(max_length=500)
    Learning_Type = models.CharField(max_length=500)
    Enrolled = models.CharField(max_length=500)
    Reviews = models.CharField(max_length=500)
    Last_Updated = models.CharField(max_length=500, default=None, null=True, blank=True)
    Category = models.CharField(max_length=100)
    #Skills = models.ForeignKey(Skill, on_delete=models.CASCADE, default=None, null=True, blank=True)
    Instructors = models.CharField(max_length=500)
    #Organization = models.CharField(max_length=500)