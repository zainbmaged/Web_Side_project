from django.db import models

# Create your models here.
class Instructor(models.Model):
    Name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    numberofcourse = models.IntegerField()
    Field = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places= 2)
    def __str__(self):
        return self.Name


class Skill(models.Model):
     type = models.CharField(max_length=500) 
     def __str__(self):
        return self.type
     
class Course(models.Model):

    
    title = models.CharField(max_length=500)
    language = models.CharField(max_length=200)
    enrolled = models.IntegerField()
    url = models.URLField(max_length=1000)
    level = models.CharField(max_length=300)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=500) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description =  models.TextField()
    syllabus = models.TextField()
    date_modified = models.DateField()
    certificated = models.BooleanField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    instructors = models.ManyToManyField(Instructor)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.title

class User(models.Model):
    ID = models.IntegerField(primary_key=True)
    Profile_Picture = models.ImageField(upload_to='PPimages')
    Email = models.CharField(max_length=100)
    Password = models.CharField(max_length=10)
    Name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course,default=None)
    skills = models.ManyToManyField(Skill,default=None)
    def cours(self):
        return self.courses
    def skill(self):
        return self.skills
