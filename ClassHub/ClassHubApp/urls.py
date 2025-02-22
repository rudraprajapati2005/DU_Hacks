from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('',views.login,name="login"),
    path('signin/',views.signin,name="signin"),
    path('home/',views.teacher_home,name="teacher_home"),
    path('home/',views.student_home,name="student_home"),
]