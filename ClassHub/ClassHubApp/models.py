from django.db import models
from django.contrib.auth.models import User

class Teacher_data(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Increased length
    subject = models.CharField(max_length=50)

class Student(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
   
    def __str__(self):
        return self.email  # Fixed issue (was referencing 'user.username')


class ClassroomCreator(models.Model):
    user_id = models.CharField(primary_key=True,max_length=255,unique=True)
    user_classroom_name = models.CharField(max_length=255,unique=True)
    user_email = models.CharField(max_length=255,unique=True)
    user_password= models.CharField( null=True,max_length=255)  # Optional field for biography

class Classroom(models.Model):
    user_id = models.ForeignKey(ClassroomCreator, on_delete=models.CASCADE)
    classroom_name = models.CharField(max_length=255,unique=True)
    classroom_code = models.CharField(max_length=255,unique=True,default='DEFAULT_CODE')
    
# class Attendence(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

#     def __str__(self):
#         return f"{self.student.user.username} - {self.classroom.classroom_name} - {self.date} - {self.status}"

class Attendance(models.Model):  # Ensure this matches the view
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])



class StudentDetails(models.Model):
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField()
    year = models.IntegerField()
    branch = models.CharField(max_length=50)
    classroom_id = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} - {self.student_id}"
    
# meetings/models.py

from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings')

class Participant(models.Model):
    MEETING_ROLES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)