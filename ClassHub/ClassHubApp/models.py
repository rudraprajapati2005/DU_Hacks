from django.db import models

class ClassroomCreator(models.Model):
    user_id = models.TextField(primary_key=True)
    user_classroom_name = models.CharField(max_length=255,unique=False)
    user_email = models.CharField(max_length=255,unique=True)
    user_password= models.TextField( null=True)  # Optional field for biography

class Classroom(models.Model):
    creator = models.ForeignKey(ClassroomCreator, on_delete=models.CASCADE)
    classroom_name = models.CharField(max_length=255,unique=True)
    
