from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.login,name="login"),
    path('signin/',views.signin,name="signin"),
    path('home/',views.teacher_home,name="teacher_home"),
    path('home/',views.student_home,name="student_home"),
]