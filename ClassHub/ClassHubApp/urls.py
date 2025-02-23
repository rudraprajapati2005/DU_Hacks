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
    path('student_home/',views.student_home,name="student_home"),
    
    # Teacher & Student Login/Signup Routes
    path('teacher-student-login/', views.teacher_student_login, name='teacher_student_login'),
    path('teacher-student-signin/',views.teacher_student_signin,name="teacher_student_signin"),
    path('student_details/',views.submit_student_details,name="submit_student_details"),
    path('classRoomCreatorLogin',views.classRoomCreatorLogin,name="classRoomCreatorLogin"),
    # path('home/',views.teacher_home,name="teacher_home"),
    # path('home/',views.student_home,name="student_home"),
    path('teacher-student-login/signin/', views.teacher_student_signin, name="teacher_student_signin"),  # ✅ Fixed
    path('onlineclass/',views.classmeet,name="classmeet"),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    # Student Details Submission
    path('student_details/', views.submit_student_details, name="submit_student_details"),  
    path('teacher-home/',views.teacher_home,name="teacher_home"),

    #save the subject of the teacher
    path('save_subject/',views.save_subject,name="teacher-save-subject"),
     # Video Conference Routes
    path('start-meeting/', views.start_meeting, name='start_meeting'),
    path('join-meeting/<int:meeting_id>/', views.join_meeting, name='join_meeting'),
  ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

