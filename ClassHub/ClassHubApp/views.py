from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from ClassHubApp.models import Teacher_data, Student
from django.contrib.auth.hashers import check_password
from ClassHubApp.models import Teacher_data, Student
from .models import Student,Classroom,ClassroomCreator
from .forms import StudentForm,classRoomForm,ClassRoomGeneratorForm
from .models import Student, Attendance
from django.shortcuts import get_object_or_404, redirect
import random

def teacher_student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and Password are required.")
            return redirect('teacher_student_login')

        user = None
        user_type = None

        try:
            user = Teacher_data.objects.get(email=email)
            print("User found in Teacher_data:", user)

            if check_password(password, user.password):  
                user_type = "teacher"
                request.session['user_id'] = user.id
                request.session['user_type'] = user_type
                return redirect('teacher_home')  # Fixed
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('teacher_student_login')

        except Teacher_data.DoesNotExist:
            pass  

        try:
            user = Student.objects.get(email=email)
            print("User found in Student:", user)

            if check_password(password, user.password):  
                user_type = "student"
                request.session['user_id'] = user.id
                request.session['user_type'] = user_type
                return redirect('student_home')  # Fixed
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('teacher_student_login')

        except Student.DoesNotExist:
            pass

        messages.error(request, "Invalid email or password.")
        return redirect('teacher_student_login')

    return render(request, 'login.html')
def teacher_student_signin(request):
    if request.method == "POST":
        try:
            # fullname = request.POST.get('fullname')
            selected_user = request.POST.get('user')  # Changed from 'role' to 'user'
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if not selected_user or not email or not password or not confirm_password:
                messages.error(request, "All fields are required.")
                return redirect('signteacher_student_signinin')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('teacher_student_signin')

            hashed_password = make_password(password)

            if selected_user == "teacher":
                Teacher_data.objects.create(email=email, password=hashed_password)
            if selected_user == "student":
                print("Saving student data...")
                Student.objects.create(email=email, password=hashed_password)

            messages.success(request, "Registration successful! Please log in.")
            return redirect('teacher_student_signin')  # Redirect after successful signup

        except Exception as e:
            print("Error:", e)
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'signin.html')

def teacher_home(request):
    return render(request, 'teacher_home.html')

def student_home(request):
    return render(request, 'student_home.html')

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
    if 'user_type' in request.session :
        if request.session['user_type'] == 'classroomCreator':
            classroomCreatorName = request.session['creator']
            classroomCreator_details = ClassroomCreator.objects.filter(user_id=classroomCreatorName)
            classroomdetails = Classroom.objects.filter(user_id=classroomCreatorName)
            
            # Extract field values
            classroomCreator_list = [
                {
                    'user_id': creator.user_id,
                    'user_classroom_name': creator.user_classroom_name,
                    'user_email': creator.user_email,
                    'user_password': creator.user_password
                }
                for creator in classroomCreator_details
            ]

            classroom_list = [
                {
                    'user_id': classroom.user_id.user_id,  # Access related ClassroomCreator user_id
                    'classroom_name': classroom.classroom_name,
                    'classroom_code': classroom.classroom_code
                }
                for classroom in classroomdetails
            ]

            return render(request, 'classRoomCreator.html', {
                'classroomCreator': classroomCreator_list,
                'classroom': classroom_list
            })
        return HttpResponse('DONE CHE')
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
            form=str(form)
            return HttpResponse('Classroom created successfully!<br>Classroom code: ' + form)
    else:
            return HttpResponse('Here Form is not valid')
 
def mark_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date = request.POST.get('date')
        status = request.POST.get('status')
        
        student = get_object_or_404(Student, id=student_id)
        attendance, created = Attendance.objects.get_or_create(student=student, date=date)
        attendance.status = status
        attendance.save()
        
        return HttpResponse('Attendance marked successfully')
    
    students = Student.objects.all()
    return render(request, 'mark_attendance.html', {'students': students})

def selection_register(request):
    return render(request,'login_after.html')

def submit_student_details(request):
    return render(request,'student_details.html')

def classRoomCreatorLogin(request):
        if request.method=='POST':
            email=request.POST.get('user_id')
            password=request.POST.get('password')
            classroomCreatorName=email
            try:
                classroomCreator=ClassroomCreator.objects.get(user_id=email)
                if classroomCreator.user_password==password:
                    classroomCreator_details = ClassroomCreator.objects.filter(user_id=classroomCreatorName)
                    classroomCreatorName=email
                    classroomdetails = Classroom.objects.filter(user_id=classroomCreatorName)
                    # Extract field values
                    classroomCreator_list = [
                        {
                            'user_id': creator.user_id,
                            'user_classroom_name': creator.user_classroom_name,
                            'user_email': creator.user_email,
                            'user_password': creator.user_password
                        }
                        for creator in classroomCreator_details
                    ]

                    classroom_list = [
                        {
                            'user_id': classroom.user_id.user_id,  # Access related ClassroomCreator user_id
                            'classroom_name': classroom.classroom_name,
                            'classroom_code': classroom.classroom_code
                        }
                        for classroom in classroomdetails
                    ]

                    return render(request, 'classRoomCreator.html', {
                        'classroomCreator': classroomCreator_list,
                        'classroom': classroom_list
                    })
                else:
                    return HttpResponse('Invalid Password')
            except ClassroomCreator.DoesNotExist:
                return HttpResponse('Invalid Email')
        return render(request,'classRoomCreatorLogin.html')