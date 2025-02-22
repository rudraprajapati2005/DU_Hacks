from django import forms
from .models import Student, Attendance


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['email', 'password']
        labels = {
            'student_id': 'Student ID',
            'department': 'Department',
            'year': 'Year',
            'section': 'Section',
            'semester': 'Semester',
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=[('Present', 'Present'), ('Absent', 'Absent')], attrs={'class': 'form-control'}),
        }
