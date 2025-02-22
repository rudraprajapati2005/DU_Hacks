from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'department', 'year', 'section', 'semester']
        labels = {
            'student_id': 'Student ID',
            'department': 'Department',
            'year': 'Year',
            'section': 'Section',
            'semester': 'Semester',
        }