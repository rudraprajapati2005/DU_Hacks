from django.shortcuts import render,HttpResponse
<<<<<<< HEAD
from .models import Student,Classroom
from .forms import StudentForm,classRoomForm,ClassRoomGeneratorForm
=======
from .models import Student, Attendence
from .forms import StudentForm
>>>>>>> 50e3b7a14c5ef3560469bf2fcb5e6f9eacd752db
from django.shortcuts import get_object_or_404, redirect
import random

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
 
            
    form = StudentForm(request.POST or None)
    if form.is_valid():
        return HttpResponse('<h1>' +form+ '</h1>')
    return render(request, 'Student_details.html', {'form': form})

def mark_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date = request.POST.get('date')
        status = request.POST.get('status')
        
        student = get_object_or_404(Student, id=student_id)
        attendance, created = Attendence.objects.get_or_create(student=student, date=date)
        attendance.status = status
        attendance.save()
        
        return HttpResponse('Attendance marked successfully')
    
    students = Student.objects.all()
    return render(request, 'mark_attendance.html', {'students': students})
