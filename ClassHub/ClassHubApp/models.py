from django.db import models
from django.contrib.auth.models import User

class Teacher_data(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Increased length
    subject = models.CharField(max_length=50)

class Student(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Increased length
    # <- Make this optional
   
    def __str__(self):
        return self.email  # Fixed issue (was referencing 'user.username')



    




# Create your models here.
