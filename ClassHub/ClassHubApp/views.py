from django.shortcuts import render,HttpResponse
from .models import Student
from .forms import StudentForm
from django.shortcuts import get_object_or_404, redirect

def Student_details(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Student_details')
    else:
        form = StudentForm()

    return render(request,'index.html', {'form': form})


    student = get_object_or_404(Student, student_id=1)
    return render(request, 'Student_details.html', {'student': student})
    

def createClassroom(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        return HttpResponse('<h1>' +form+ '</h1>')
    return render(request, 'Student_details.html', {'form': form})
