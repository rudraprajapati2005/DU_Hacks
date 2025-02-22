from django.contrib import admin
from .models import Student, Teacher_data, ClassroomCreator, Classroom, Attendence

admin.site.register(Student)
admin.site.register(Teacher_data)
admin.site.register(ClassroomCreator)
admin.site.register(Classroom)
admin.site.register(Attendence)

# Register your models here.
