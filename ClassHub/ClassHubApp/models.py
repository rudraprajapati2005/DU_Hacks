from django.db import models
from django.contrib.auth.models import User

class Teacher_data(models.Model):
    email =models.CharField( max_length=50)
    password =models.CharField(max_length=10)
    subject =models.CharField(max_length=10)

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

class ClassroomCreator(models.Model):
    user_id = models.TextField(primary_key=True)
    user_classroom_name = models.CharField(max_length=255,unique=False)
    user_email = models.CharField(max_length=255,unique=True)
    user_password= models.TextField( null=True)  # Optional field for biography

class Classroom(models.Model):
    creator = models.ForeignKey(ClassroomCreator, on_delete=models.CASCADE)
    classroom_name = models.CharField(max_length=255,unique=True)
    
