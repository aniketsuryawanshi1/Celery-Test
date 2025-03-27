# home/views.py
from django.shortcuts import render
from .models import Student

def homePage(request):
    students = Student.objects.all()
    context = {"students": students}
    return render(request, 'index.html', context=context)