from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
<<<<<<< HEAD
    path('',views.login,name="login"),
    path('signin/',views.signin,name="signin"),
    path('home/',views.teacher_home,name="teacher_home"),
    path('home/',views.student_home,name="student_home"),
=======
    path('', views.Student_details, name='Student_details'),  
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),    
    path('admin/', admin.site.urls),
>>>>>>> 50e3b7a14c5ef3560469bf2fcb5e6f9eacd752db
]