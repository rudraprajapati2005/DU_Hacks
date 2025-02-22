from django.shortcuts import render
from .models import Student
from .forms import StudentForm
from django.shortcuts import get_object_or_404, redirect

def Student_details(request):

    student = get_object_or_404(Student, Student_id=1)
    return render(request, 'Student_details.html', {'student': student})
    



# Create your views here.
