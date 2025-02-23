from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from . import views 
urlpatterns = [
    path('', views.Student_details, name='Student_details'),    
    path('createClassroom/', views.createClassroom, name='createClassroom'),  
    path('generateClassroomCode/', views.generateClassroom, name='generateClassroom'),  
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),    
    path('selection-register/', views.selection_register, name='after-login'),
    
    # Teacher & Student Login/Signup Routes
    path('teacher-student-login/', views.teacher_student_login, name='teacher_student_login'),
    path('teacher-student-login/signin/', views.teacher_student_signin, name="teacher_student_signin"),  # ✅ Fixed
    

    # Student Details Submission
    path('student_details/', views.submit_student_details, name="submit_student_details"),  
]


