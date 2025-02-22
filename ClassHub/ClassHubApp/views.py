from django.shortcuts import render
from .models import Student
# from .forms import 
from django.shortcuts import get_object_or_404, redirect

def Student_details(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'Student_details.html', {'student': student})
    



# Create your views here.
