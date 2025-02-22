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


class ClassroomCreator(models.Model):
    user_id = models.TextField(primary_key=True)
    user_classroom_name = models.CharField(max_length=255,unique=False)
    user_email = models.CharField(max_length=255,unique=True)
    user_password= models.TextField( null=True)  # Optional field for biography

class Classroom(models.Model):
    creator = models.ForeignKey(ClassroomCreator, on_delete=models.CASCADE)
    classroom_name = models.CharField(max_length=255,unique=True)
    
class Attendence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

<<<<<<< HEAD

=======
    def __str__(self):
        return f"{self.student.user.username} - {self.classroom.classroom_name} - {self.date} - {self.status}"
>>>>>>> 50e3b7a14c5ef3560469bf2fcb5e6f9eacd752db


