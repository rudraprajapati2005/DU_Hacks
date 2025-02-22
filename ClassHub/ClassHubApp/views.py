<<<<<<< HEAD
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from ClassHubApp.models import Teacher_data, Student

from django.contrib.auth.hashers import check_password

from ClassHubApp.models import Teacher_data, Student
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and Password are required.")
            return redirect('login')

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
                return redirect('login')

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
                return redirect('login')

        except Student.DoesNotExist:
            pass

        messages.error(request, "Invalid email or password.")
        return redirect('login')

    return render(request, 'login.html')
def signin(request):
    if request.method == "POST":
        try:
            # fullname = request.POST.get('fullname')
            selected_user = request.POST.get('user')  # Changed from 'role' to 'user'
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if not selected_user or not email or not password or not confirm_password:
                messages.error(request, "All fields are required.")
                return redirect('signin')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('signin')

            hashed_password = make_password(password)

            if selected_user == "teacher":
                Teacher_data.objects.create(email=email, password=hashed_password)
            if selected_user == "student":
                print("Saving student data...")
                Student.objects.create(email=email, password=hashed_password)

            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Redirect after successful signup

        except Exception as e:
            print("Error:", e)
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'signin.html')

def teacher_home(request):
    return render(request, 'teacher_home.html')

def student_home(request):
    return render(request, 'student_home.html')
=======
from django.shortcuts import render,HttpResponse
from .models import Student, Attendence
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
>>>>>>> 50e3b7a14c5ef3560469bf2fcb5e6f9eacd752db
