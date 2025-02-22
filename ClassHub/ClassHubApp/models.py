from django.db import models
from django.contrib.auth.models import User


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


    




# Create your models here.
