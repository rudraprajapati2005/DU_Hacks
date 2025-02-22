from django import forms
from .models import Student,ClassroomCreator,Classroom


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['email', 'password']
        labels = {
            'email': 'Student Email ID',
            'password': 'Password',
        }
class classRoomForm(forms.ModelForm):
    class Meta:
        model = ClassroomCreator
        fields = ['user_id','user_classroom_name', 'user_email', 'user_password']
        labels = {
            'user_id': 'User ID',
            'user_classroom_name': 'Classroom Name',
            'user_email': 'Email',
            'user_password': 'Password',
        }
        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'user_classroom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
class ClassRoomGeneratorForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['user_id', 'classroom_name', 'classroom_code']
