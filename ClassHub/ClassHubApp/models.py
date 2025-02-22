from django.db import models
from django.contrib.auth.models import User

class Teacher_data(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Increased length
    subject = models.CharField(max_length=50)

class Student(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255,min_length=8)
   
    def __str__(self):
        return self.email  # Fixed issue (was referencing 'user.username')


class ClassroomCreator(models.Model):
    user_id = models.CharField(primary_key=True,max_length=255,unique=True)
    user_classroom_name = models.CharField(max_length=255,unique=False)
    user_email = models.CharField(max_length=255,unique=True)
    user_password= models.CharField( null=True,max_length=255)  # Optional field for biography

class Classroom(models.Model):
    user_id = models.ForeignKey(ClassroomCreator, on_delete=models.CASCADE)
    classroom_name = models.CharField(max_length=255,unique=True)
    classroom_code = models.CharField(max_length=255,unique=True,default='DEFAULT_CODE')
    
class Attendence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])



