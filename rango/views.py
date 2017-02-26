from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Student


# add @login_required
def all_students(request):

    student_list = Student.objects.order_by('guid')

    context_dict = { 'students': student_list }

    return render(request, 'nucleus/students.html', context=context_dict)
