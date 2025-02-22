from django.db import models
from django.contrib.auth.models import User

class Teacher_data(models.Model):
    email =models.CharField( max_length=50)
    password =models.CharField(max_length=10)
    subject =models.CharField(max_length=10)

<<<<<<< HEAD
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    section = models.CharField(max_length=1)
    semester = models.IntegerField()
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    



=======
    def __str__(self):
        return self.email
    
>>>>>>> c6392c86d02f9b0adb6d048c28b7e4f67ade39e6

# Create your models here.
