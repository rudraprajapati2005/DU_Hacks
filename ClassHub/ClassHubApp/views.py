from django.shortcuts import render, HttpResponse
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


    



# Create your views here.
