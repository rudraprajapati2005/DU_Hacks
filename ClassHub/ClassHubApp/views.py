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
