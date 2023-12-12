from django.db import models

# Create your models here.
class Instructor(models.Model):
    Name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    numberofcourse = models.IntegerField()
    Field = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places= 2)

class User(models.Model):
    ID = models.IntegerField(primary_key=True)
    Profile_Picture = models.ImageField(upload_to='PPimages')
    Email = 
    Password = 
    Name = 
