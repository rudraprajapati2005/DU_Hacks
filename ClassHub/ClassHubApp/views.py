from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from ClassHubApp.models import Teacher_data, Student
from django.contrib.auth.hashers import check_password
from ClassHubApp.models import Teacher_data, Student
from .models import Student,Classroom,ClassroomCreator
from .forms import StudentForm,classRoomForm,ClassRoomGeneratorForm
from .models import Student, Attendance,Meeting,Participant
from django.shortcuts import get_object_or_404, redirect
import random
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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
                request.session['user_id'] = user.email
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
               
                teachers = Teacher_data.objects.all() 
                return render(request,'Student_home.html', {'teachers': teachers})  # Fixed
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

def classmeet(request):
    return render(request,'classmeet.html')

def student_home(request):
    return render(request,'Student_home.html')

def teacher_dashboard(request):
    # Fetch all teacher records
    return render(request, 'Student_home.html', {'teachers': teachers}) 
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
def teacher_home(request):
        teacher = Teacher_data.objects.filter(email=request.session['user_id']).first()

    # Convert the teacher data into a dictionary
        teacher_data = {
            'email': teacher.email,
            'password': teacher.password,  # Be cautious with sensitive information
            'subject': teacher.subject,
        }
        # Pass the dictionary to the template
        return render(request, 'teacher_home.html', {'teacher': teacher_data})

def save_subject(request):
    if request.method == 'POST':
        teacher = Teacher_data.objects.filter(email=request.POST.get('teacher_id')).first()
        teacher.subject = request.POST.get('subject')
        teacher.save()
        teacher = Teacher_data.objects.filter(email=request.POST.get('teacher_id')).first()
        teacher_data = {
            'email': teacher.email,
            'password': teacher.password,  # Be cautious with sensitive information
            'subject': teacher.subject,
        }
        return render(request, 'teacher_home.html', {'teacher': teacher_data})
    return HttpResponse('Invalid request')


class VideoMeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'meeting_{self.room_name}'

        # Add the participant to the meeting
        await self.add_participant(self.room_name, self.scope['user'])

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Remove the participant from the meeting
        await self.remove_participant(self.room_name, self.scope['user'])

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    
    @database_sync_to_async
    def add_participant(self, room_name, user):
        meeting = Meeting.objects.get(id=room_name)
        Participant.objects.create(meeting=meeting, user=user, role=self.get_user_role(user))

    @database_sync_to_async
    def remove_participant(self, room_name, user):
        meeting = Meeting.objects.get(id=room_name)
        Participant.objects.filter(meeting=meeting, user=user).delete()

    def get_user_role(self, user):
        if Teacher_data.objects.filter(email=user.email).exists():
            return 'Teacher'
        elif Student.objects.filter(email=user.email).exists():
            return 'Student'
        else:
            return 'Unknown'
def start_meeting(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_time = timezone.now()
        created_by = request.user

        meeting = Meeting.objects.create(title=title, start_time=start_time, created_by=created_by)
        return redirect('join_meeting', meeting_id=meeting.id)
    
    return render(request, 'start_meeting.html')


def join_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    if request.user.is_authenticated:
        Participant.objects.get_or_create(meeting=meeting, user=request.user)
    
    return render(request, 'join_meeting.html', {'meeting': meeting})
