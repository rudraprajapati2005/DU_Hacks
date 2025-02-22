from django.shortcuts import render,HttpResponse
from .models import Student,Classroom
from .forms import StudentForm,classRoomForm,ClassRoomGeneratorForm
from django.shortcuts import get_object_or_404, redirect
import random

def Student_details(request):
    student = get_object_or_404(Student, student_id=1)
    return render(request, 'Student_details.html', {'student': student})
    

def createClassroom(request):
    form=classRoomForm()
    if request.method == 'POST':
        form = classRoomForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['creator'] = form.cleaned_data['user_id']
            request.session['user_type'] = 'classroomCreator'
            request.session['classroom_name'] = form.cleaned_data['user_classroom_name']
            return redirect('generateClassroom')
    return render(request, 'admin_classroomCreate.html', {'form': form})

def generateClassroom(request):
    chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@+/*-!@#$%^`*')
    length = 15
    password = ''.join(random.choice(chars) for _ in range(length))
    
    while Classroom.objects.filter(classroom_code=password).exists():
        password = ''.join(random.choice(chars) for _ in range(length))
    

    creator = request.session['creator'] # Match the form field name
    classroom_name = request.session['classroom_name']
    classroom_code = password
        
    form = ClassRoomGeneratorForm(data={
            'user_id': creator,
            'classroom_name': classroom_name,
            'classroom_code': classroom_code
        })
        
    if form.is_valid():
            form.save()
            form=form.__str__
            return HttpResponse('Classroom created successfully!<br>Classroom code: ' + form)
    else:
            return HttpResponse('Form is not valid')
 
            
