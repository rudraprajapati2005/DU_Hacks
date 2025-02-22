from django.db import models
from django.contrib.auth.models import User

class Teacher_data(models.Model):
    email =models.CharField( max_length=50)
    password =models.CharField(max_length=10)
    subject =models.CharField(max_length=10)

    def __str__(self):
        return self.email
    

# Create your models here.
