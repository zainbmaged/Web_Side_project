from django.db import models

# Create your models here.
class instructor(models.Model):
    Name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    numberofcourse = models.IntegerField()
    Field = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places= 2)